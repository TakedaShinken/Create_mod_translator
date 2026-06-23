import json
import zipfile
from pathlib import Path
from typing import Dict

def generate_resource_pack(lang_data: Dict[str, str], pack_format: int, modid: str, output_path: str):
    """
    翻訳データからリソースパック(ZIP)を生成する。
    """
    output_path = Path(output_path)
    if output_path.suffix != '.zip':
        output_path = output_path.with_suffix('.zip')
        
    mcmeta = {
        "pack": {
            "pack_format": pack_format,
            "description": f"Japanese Translation for {modid}"
        }
    }
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # pack.mcmeta を書き込む
        zipf.writestr("pack.mcmeta", json.dumps(mcmeta, indent=2, ensure_ascii=False))
        
        # ja_jp.json を書き込む
        lang_path = f"assets/{modid}/lang/ja_jp.json"
        zipf.writestr(lang_path, json.dumps(lang_data, indent=2, ensure_ascii=False))
        
    print(f"Generated resource pack at: {output_path.absolute()}")
