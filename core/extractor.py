import zipfile
import json
import re
from pathlib import Path
from typing import Dict, Any, Tuple

PACK_FORMATS = {
    "1.18": 8, "1.18.1": 8, "1.18.2": 8,
    "1.19": 9, "1.19.1": 9, "1.19.2": 9,
    "1.19.3": 12, "1.19.4": 13,
    "1.20": 15, "1.20.1": 15,
    "1.20.2": 18,
    "1.20.3": 22, "1.20.4": 22,
    "1.20.5": 32, "1.20.6": 32,
    "1.21": 34, "1.21.1": 34,
    "1.21.2": 42, "1.21.3": 42
}

def guess_mc_version_from_filename(filename: str) -> str | None:
    match = re.search(r'(1\.\d{2}(?:\.\d+)?)', filename)
    if match:
        return match.group(1)
    return None

def extract_lang_and_metadata(jar_path: str | Path) -> Tuple[Dict[str, str], int, str]:
    """
    JARファイルから言語ファイル(en_us.json)を抽出し、Minecraftバージョンを推測して pack_format と mod_id を返します。
    """
    jar_path = Path(jar_path)
    if not jar_path.exists():
        raise FileNotFoundError(f"Mod JAR not found: {jar_path}")
        
    mc_version = guess_mc_version_from_filename(jar_path.name)
    pack_format = PACK_FORMATS.get(mc_version, 15) if mc_version else 15
    
    lang_data = {}
    modid = "create"

    with zipfile.ZipFile(jar_path, 'r') as jar:
        lang_files = [name for name in jar.namelist() if name.startswith('assets/') and name.endswith('/lang/en_us.json')]
        
        if not lang_files:
            raise ValueError("No en_us.json found in the JAR file.")
            
        # minecraftやforgeなど、Mod本体以外のリソースを除外する
        valid_files = [lf for lf in lang_files if not any(lf.startswith(f"assets/{x}/") for x in ["minecraft", "forge", "fabric", "c"])]
        if not valid_files:
            valid_files = lang_files
            
        target_file = valid_files[0]
        for lf in valid_files:
            if 'assets/create/lang/' in lf:
                target_file = lf
                break
                
        modid = target_file.split('/')[1]
        
        with jar.open(target_file) as f:
            content = f.read().decode('utf-8')
            try:
                lang_data = json.loads(content)
            except json.JSONDecodeError as e:
                # Modの言語ファイルには厳密なJSONではない場合があるため、基本は標準パーサーを使用
                raise RuntimeError(f"Failed to parse JSON in {target_file}: {e}")

    return lang_data, pack_format, modid
