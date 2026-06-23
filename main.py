import argparse
import sys
from pathlib import Path
from core.extractor import extract_lang_and_metadata
from core.parser import parse_lang_data, build_lang_data
from core.generator import generate_resource_pack
from translator.gemma import OpenAITranslator

def main():
    parser = argparse.ArgumentParser(description="Minecraft Create Mod 日本語化リソースパック自動生成ツール")
    parser.add_argument("jar_file", help="翻訳対象のMod JARファイルのパス")
    parser.add_argument("-o", "--output", default="output_resource_pack.zip", help="出力するリソースパックのZIPファイル名")
    parser.add_argument("--api-url", default="http://localhost:11434/v1/chat/completions", help="OpenAI互換APIのエンドポイントURL (デフォルト: Ollama local API)")
    parser.add_argument("--model", default="gemma", help="使用するモデル名")
    parser.add_argument("--api-key", default="dummy", help="APIキー (Ollama/LM Studioの場合は不要)")
    parser.add_argument("--limit", type=int, default=None, help="テスト用: 翻訳するキーの最大数を制限する")
    parser.add_argument("--lm-studio", action="store_true", help="LM Studioを利用する (API URLとモデル名を自動設定)")
    
    args = parser.parse_args()
    
    if args.lm_studio:
        # ユーザーが明示的に上書きしていない場合、LM Studioのデフォルト値に変更
        if args.api_url == "http://localhost:11434/v1/chat/completions":
            args.api_url = "http://localhost:1234/v1/chat/completions"
        if args.model == "gemma":
            args.model = "local-model"
            
    jar_path = Path(args.jar_file)
    if not jar_path.exists():
        print(f"Error: JAR file not found - {jar_path}")
        sys.exit(1)
        
    print(f"--- Mod JAR 抽出 ---")
    print(f"File: {jar_path.name}")
    try:
        lang_dict, pack_format, modid = extract_lang_and_metadata(jar_path)
        print(f"Detected Mod ID: {modid}")
        print(f"Inferred Pack Format: {pack_format}")
        print(f"Found {len(lang_dict)} translation keys.")
    except Exception as e:
        print(f"Extraction failed: {e}")
        sys.exit(1)
        
    print(f"\n--- 翻訳タスクの分類 ---")
    tasks = parse_lang_data(lang_dict)
    
    if args.limit:
        print(f"Limiting tasks to {args.limit} for testing...")
        tasks = tasks[:args.limit]
    
    print(f"Initializing translator using model '{args.model}' at '{args.api_url}'...")
    translator = OpenAITranslator(api_url=args.api_url, model_name=args.model, api_key=args.api_key)
    
    translator.translate_tasks(tasks)
    
    print(f"\n--- リソースパック生成 ---")
    translated_dict = build_lang_data(tasks)
    generate_resource_pack(translated_dict, pack_format, modid, args.output)
    
    print("\nすべての処理が完了しました！")

if __name__ == "__main__":
    main()
