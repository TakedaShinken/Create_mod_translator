# Create Mod Japanese Resource Pack Generator
[English](#english) | [日本語](#japanese)

---

<a id="japanese"></a>
## 🇯🇵 日本語

Minecraftの「Create」系Mod（本体および各種アドオン）向けの日本語化リソースパックを、ローカルAI（LLM）を用いて全自動で生成するPythonツールです。

### 特徴
- **多様なAIモデルに対応**: `gemma`, `phi`, `llama3`, `qwen` など、OllamaやLM Studioで動くOpenAI互換APIを持つあらゆるモデルに対応しています。
- **文脈を理解した翻訳**: 実績テキストやアイテム名を自然な日本語に翻訳します。
- **Ponder（Wキーチュートリアル）対応**: Create特有の長文チュートリアルテキストの文脈の繋がりや、プレースホルダー、カラーコードを破壊せずに翻訳します。
- **アドオンの自動判定**: `.jar` ファイルを渡すだけで自動的にアドオン名を判定してリソースパックを構築します。
- **翻訳辞書機能**: 固有名詞や特定の用語の翻訳ルールを自由に定義可能です。
- **フリーズ防止と再開機能**: 途中でエラーが起きてもキャッシュから瞬時に再開できます。

### インストール
```bash
git clone https://github.com/yourusername/create_mod_japanese.git
cd create_mod_japanese
pip install -r requirements.txt
```

### 使い方
1. Ollama または LM Studio を起動します。
2. ツールの実行:

**Ollamaを使用する場合 (デフォルトモデル: gemma):**
```bash
python main.py "path/to/create-addon-1.20.1.jar" --output "ja_jp_pack.zip"
```

**モデルを変更する場合 (例: phi):**
```bash
python main.py "path/to/create-addon-1.20.1.jar" --model "phi"
```

**LM Studioを使用する場合:**
```bash
python main.py "path/to/create-addon-1.20.1.jar" --lm-studio
```

---

<a id="english"></a>
## 🇬🇧 English

A Python tool that fully automates the generation of Japanese localization resource packs for Minecraft "Create" mod and its addons using Local AI (LLMs).

### Features
- **Multi-Model Support**: Supports `gemma`, `phi`, `llama3`, `qwen` and any other model that runs on Ollama or LM Studio via OpenAI compatible APIs.
- **Context-Aware Translation**: Translates achievements and item names into natural Japanese.
- **Ponder Support**: Safely translates multi-line Ponder tutorials without breaking placeholders or color codes.
- **Auto Addon Detection**: Just provide the `.jar` file, and it automatically infers the addon ID and `pack_format`.
- **Glossary Feature**: Define your own translation rules for proper nouns and specific terms.
- **Resume & Timeout Protection**: Automatically caches progress to resume instantly in case of AI hallucinations or crashes.

### Installation
```bash
git clone https://github.com/yourusername/create_mod_japanese.git
cd create_mod_japanese
pip install -r requirements.txt
```

### Usage
1. Start Ollama or LM Studio local server.
2. Run the tool:

**Using Ollama (Default model: gemma):**
```bash
python main.py "path/to/create-addon-1.20.1.jar" --output "ja_jp_pack.zip"
```

**Using a different model (e.g. phi):**
```bash
python main.py "path/to/create-addon-1.20.1.jar" --model "phi"
```

**Using LM Studio:**
```bash
python main.py "path/to/create-addon-1.20.1.jar" --lm-studio
```

### Glossary Configuration
Edit `dictionary.json` to control translation behaviors.
- `do_not_translate`: List of exact strings to keep in English (e.g., Mod names).
- `force_translate`: Map of specific translations (e.g., "Andesite": "安山岩").

### License
[MIT License](LICENSE)
