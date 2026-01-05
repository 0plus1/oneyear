from dataclasses import dataclass
from pathlib import Path
from typing import Optional

A0_SHORT_MM = 841.0
A0_LONG_MM = 1189.0

@dataclass
class Config:
    input_dir: Path
    out_path: Path

    dpi: int = 300
    square_mm: float = A0_SHORT_MM

    gutter_px: int = 10
    outer_margin_px: int = 80

    rows: Optional[int] = None
    cols: Optional[int] = None

    center_box_h_cells: int = 5
    center_box_w_cells: int = 7

    title: str = "2025"
    subtitle: str = "A year in photos"

    font_path: Optional[str] = None
    title_size: int = 220
    subtitle_size: int = 90
    title_color: str = "#111111"
    subtitle_color: str = "#333333"
    box_bg: str = "white"
    text_padding_px: int = 80

    preview_scale: float = 1.0
    draw_text: bool = True
