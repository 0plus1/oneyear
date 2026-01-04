from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from PIL import Image

def _parse_exif_dt(exif_value: str) -> Optional[datetime]:
    try:
        return datetime.strptime(exif_value, "%Y:%m:%d %H:%M:%S")
    except Exception:
        return None

def photo_datetime(path: Path) -> datetime:
    """
    DateTimeOriginal (36867) -> DateTime (306) -> file mtime.
    """
    try:
        with Image.open(path) as im:
            exif = im.getexif()
            dt_original = exif.get(36867)
            if isinstance(dt_original, str):
                dt = _parse_exif_dt(dt_original)
                if dt:
                    return dt

            dt_general = exif.get(306)
            if isinstance(dt_general, str):
                dt = _parse_exif_dt(dt_general)
                if dt:
                    return dt
    except Exception:
        pass

    ts = path.stat().st_mtime
    return datetime.fromtimestamp(ts)