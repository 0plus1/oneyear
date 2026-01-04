from pathlib import Path
from typing import List

def list_images(input_dir: Path) -> List[Path]:
    # HEIC included
    exts = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".heic", ".heif"}
    return [p for p in input_dir.rglob("*") if p.is_file() and p.suffix.lower() in exts]