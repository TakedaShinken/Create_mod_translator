import httpx
import json
from pathlib import Path
from tqdm import tqdm
from typing import List
from core.parser import TranslationTask
from .base import BaseTranslator

class OpenAITranslator(BaseTranslator):
    """
    OpenAI互換API (Ollama, LM Studio, OpenAI APIなど) を用いた翻訳クラス
    """
    def __init__(self, api_url: str = "http://localhost:11434/v1/chat/completions", model_name: str = "gemma", api_key: str = "dummy"):
        self.api_url = api_url
        self.model_name = model_name
        self.api_key = api_key
        # 通信がハングするのを防ぐため、読み込み（read）の最大待ち時間を60秒に制限
        self.client = httpx.Client(timeout=httpx.Timeout(10.0, read=60.0, write=20.0, pool=10.0))
        self.cache_file = Path("translation_cache.json")
        self.dict_file = Path("dictionary.json")
        self.dictionary = self._load_dictionary()

    def _load_dictionary(self) -> dict:
        if self.dict_file.exists():
            try:
                with open(self.dict_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _get_system_message(self, category: str) -> str:
        base = "あなたはMinecraftのModの専門翻訳AIです。ユーザーが与えた英語のテキストを必ず自然な日本語に翻訳してください。出力は翻訳結果のテキストのみとし、解説や挨拶などの余計な出力は一切行わないでください。"
        
        # 辞書のルールを追加
        dict_rules = ""
        if self.dictionary:
            do_not_translate = self.dictionary.get("do_not_translate", [])
            force_translate = self.dictionary.get("force_translate", {})
            if do_not_translate:
                dict_rules += "\n【重要】以下の固有名詞（Mod名など）は絶対に翻訳せず、英語のまま残してください: " + ", ".join(do_not_translate) + "。"
            if force_translate:
                dict_rules += "\n【重要】以下の単語は指定された訳語を優先して使用してください: "
                dict_rules += ", ".join([f"'{k}'->'{v}'" for k, v in force_translate.items()]) + "。"
            dict_rules += "\n上記で指定された例外を除き、アイテム名や説明文は【必ず日本語に翻訳】してください。単語を英語のまま放置しないでください。"

        if category == "item_block":
            return base + dict_rules + "\n\nこれはアイテム名・ブロック名です。ゲーム内の名称として自然な体言止めで訳してください。"
        elif category == "advancement":
            return base + dict_rules + "\n\nこれは実績のタイトルまたは説明文です。"
        elif category == "ponder_tooltip":
            return base + dict_rules + "\n\nこれはアイテムの長文説明やチュートリアル文（Ponder）の一部です。「%s」や「%1$s」などの変数プレースホルダー、「§」で始まるカラーコードは絶対にそのまま残してください。"
        else:
            return base + dict_rules

    def _load_cache(self) -> dict:
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_cache(self, cache: dict):
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)

    def translate_tasks(self, tasks: List[TranslationTask]) -> None:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 途中から再開できるようにキャッシュを読み込む
        cache = self._load_cache()
        
        progress_bar = tqdm(tasks, desc=f"Translating ({self.model_name})")
        for task in progress_bar:
            # キャッシュ済みならスキップ
            if task.key in cache:
                task.translated_text = cache[task.key]
                continue
                
            # 長いキー名の後半だけを表示
            progress_bar.set_postfix(key=task.key[-20:])
            
            system_msg = self._get_system_message(task.category)
            
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": task.original_text}
                ],
                "temperature": 0.1,
                "max_tokens": 500  # AIが暴走してフリーズするのを防ぐ
            }
            
            try:
                response = self.client.post(self.api_url, json=payload, headers=headers)
                response.raise_for_status()
                result = response.json()
                translated = result["choices"][0]["message"]["content"].strip()
                task.translated_text = translated if translated else task.original_text
                
                # 成功したらキャッシュに保存
                cache[task.key] = task.translated_text
                self._save_cache(cache)
                
            except httpx.TimeoutException:
                tqdm.write(f"\n[Timeout] Error translating '{task.key}': モデルからの応答が60秒以上ありませんでした。スキップします。")
                task.translated_text = task.original_text
            except Exception as e:
                tqdm.write(f"\n[Error] translating '{task.key}': {e}")
                task.translated_text = task.original_text
