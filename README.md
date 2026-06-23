# Create Mod Japanese Resource Pack Generator

Minecraftの「Create」系Mod（本体および各種アドオン）向けの日本語化リソースパックを、ローカルAI（LLM）を用いて全自動で生成するPythonツールです。

## 特徴
- **AIによる文脈を理解した翻訳**: GemmaなどのローカルAIを活用し、実績テキストやアイテム名を自然な日本語に翻訳します。
- **Ponder（Wキーチュートリアル）対応**: Create特有の長文チュートリアルテキストの文脈の繋がりや、`%s` などのプレースホルダー、カラーコードを破壊せずに翻訳します。
- **アドオンの自動判定**: `.jar` ファイルを渡すだけで、システムが自動的にアドオン名と `pack_format` (Minecraftバージョン) を判定してリソースパックを構築します。
- **翻訳辞書機能**: 固有名詞や特定の用語の翻訳ルールを自由に定義可能です。
- **フリーズ防止と再開機能**: ローカルAI特有のハルシネーション（無限生成）を検知してタイムアウトさせる機能や、途中から翻訳を再開できるキャッシュ機能を搭載しています。

## 動作環境
- Python 3.10 以上
- Ollama または LM Studio （ローカルAIサーバーとして利用）

## インストール

```bash
git clone https://github.com/yourusername/create_mod_japanese.git
cd create_mod_japanese
pip install -r requirements.txt
```

## 使い方

1. **AIサーバーの起動**
   - **Ollamaの場合**: `ollama run gemma` などでAPIを立ち上げておきます。
   - **LM Studioの場合**: Local Server を起動しておきます（デフォルトポート: `1234`）。

2. **ツールの実行**
   対象となるModの `.jar` ファイルを指定してツールを実行します。

   **LM Studioを使用する場合:**
   ```bash
   python main.py "path/to/create-addon-1.20.1.jar" --output "ja_jp_pack.zip" --lm-studio
   ```

   **Ollamaを使用する場合:**
   ```bash
   python main.py "path/to/create-addon-1.20.1.jar" --output "ja_jp_pack.zip"
   ```

3. **リソースパックの導入**
   出力された `.zip` ファイルを、Minecraftの `resourcepacks` フォルダにそのまま導入して有効化してください。

## 辞書機能（カスタマイズ）
ツールと同じディレクトリにある `dictionary.json` を編集することで、AIの翻訳挙動を制御できます。
- `do_not_translate`: 英語のまま残す固有名詞（Mod名など）を指定します。
- `force_translate`: 特定の英語に対する日本語訳を指定します（例: "Andesite" -> "安山岩"）。

## ライセンス
このプロジェクトは [MIT License](LICENSE) の下で公開されています。自由に改変・再配布が可能です。
