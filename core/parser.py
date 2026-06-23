from typing import Dict, List

class TranslationTask:
    def __init__(self, key: str, original_text: str, category: str):
        self.key = key
        self.original_text = original_text
        self.category = category
        self.translated_text = ""

def categorize_key(key: str) -> str:
    """キーを元にカテゴリを判定する"""
    if key.startswith("item.") or key.startswith("block."):
        return "item_block"
    elif key.startswith("advancement."):
        return "advancement"
    elif "ponder." in key or "tooltip." in key:
        return "ponder_tooltip"
    elif "gui." in key:
        return "gui"
    else:
        return "general"

def parse_lang_data(lang_data: Dict[str, str]) -> List[TranslationTask]:
    """言語データの辞書を TranslationTask のリストに変換してカテゴリ分けを行う"""
    tasks = []
    for key, text in lang_data.items():
        if not text.strip():
            continue
        category = categorize_key(key)
        tasks.append(TranslationTask(key, text, category))
    return tasks

def build_lang_data(tasks: List[TranslationTask]) -> Dict[str, str]:
    """翻訳済みのタスクリストから辞書を再構築する"""
    return {task.key: task.translated_text or task.original_text for task in tasks}
