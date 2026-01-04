import os
import re
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_w: int) -> List[str]:
    if not text:
        return []
    words = re.split(r"\s+", text.strip())
    lines: List[str] = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_center_text(
    canvas: Image.Image,
    box_px: Tuple[int, int, int, int],
    title: str,
    subtitle: str,
    font_path: Optional[str],
    title_size: int,
    subtitle_size: int,
    title_color: str,
    subtitle_color: str,
    box_bg: str,
    padding_px: int,
):
    draw = ImageDraw.Draw(canvas)
    x0, y0, x1, y1 = box_px

    # background fill
    draw.rectangle([x0, y0, x1, y1], fill=box_bg)

    if font_path and os.path.exists(font_path):
        title_font = ImageFont.truetype(font_path, title_size)
        subtitle_font = ImageFont.truetype(font_path, subtitle_size)
    else:
        print("WARNING: No font provided or font not found. Falling back to default PIL font.")
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    inner_x0 = x0 + padding_px
    inner_y0 = y0 + padding_px
    inner_x1 = x1 - padding_px
    inner_y1 = y1 - padding_px
    inner_w = inner_x1 - inner_x0
    inner_h = inner_y1 - inner_y0

    title_lines = _wrap_text(draw, title, title_font, inner_w)
    subtitle_lines = _wrap_text(draw, subtitle, subtitle_font, inner_w)

    def block_height(lines: List[str], font: ImageFont.FreeTypeFont, gap: int) -> int:
        if not lines:
            return 0
        hs = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            hs.append(bbox[3] - bbox[1])
        return sum(hs) + gap * (len(lines) - 1)

    gap_title = max(6, title_size // 6)
    gap_sub = max(6, subtitle_size // 6)
    between = max(10, title_size // 3) if title_lines and subtitle_lines else 0

    title_h = block_height(title_lines, title_font, gap_title)
    sub_h = block_height(subtitle_lines, subtitle_font, gap_sub)
    total_h = title_h + between + sub_h

    y = inner_y0 + max(0, (inner_h - total_h) // 2)

    def draw_lines(lines: List[str], font: ImageFont.FreeTypeFont, color: str, y: int, gap: int) -> int:
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            x = inner_x0 + (inner_w - w) // 2
            draw.text((x, y), line, font=font, fill=color)
            y += h + gap
        return y

    y = draw_lines(title_lines, title_font, title_color, y, gap_title)
    y += between
    _ = draw_lines(subtitle_lines, subtitle_font, subtitle_color, y, gap_sub)

def fit_rect_to_aspect(box_px: tuple[int, int, int, int], aspect: float) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = box_px
    w = x1 - x0
    h = y1 - y0

    # target: new_w / new_h = aspect, and it must fit inside (w, h)
    if w / h > aspect:
        # too wide -> limit by height
        new_h = h
        new_w = int(round(new_h * aspect))
    else:
        # too tall -> limit by width
        new_w = w
        new_h = int(round(new_w / aspect))

    nx0 = x0 + (w - new_w) // 2
    ny0 = y0 + (h - new_h) // 2
    nx1 = nx0 + new_w
    ny1 = ny0 + new_h
    return nx0, ny0, nx1, ny1