from __future__ import annotations

from pathlib import Path
from typing import List

from PIL import Image, ImageOps

# HEIC support
from pillow_heif import register_heif_opener
register_heif_opener()

Image.MAX_IMAGE_PIXELS = None

from .config import Config
from .discovery import list_images
from .exif_sort import photo_datetime
from .grid import center_box_cells, in_center_box, mm_to_px, resolve_grid
from .text_block import draw_center_text

def fit_center_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    img = ImageOps.exif_transpose(img)
    return ImageOps.fit(img, (target_w, target_h), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))

def render(cfg: Config) -> None:
    
    scale = cfg.preview_scale

    outer_margin = max(1, int(cfg.outer_margin_px * scale))
    gutter = max(1, int(cfg.gutter_px * scale))
    text_padding = max(1, int(cfg.text_padding_px * scale))

    # canvas
    side_px = mm_to_px(cfg.square_mm, cfg.dpi)
    if cfg.preview_scale != 1.0:
        side_px = max(800, int(side_px * cfg.preview_scale))

    photos = list_images(cfg.input_dir)
    if not photos:
        raise RuntimeError(f"No images found in {cfg.input_dir}")

    photos_sorted = sorted(photos, key=photo_datetime)

    reserved = cfg.center_box_h_cells * cfg.center_box_w_cells
    rows, cols = resolve_grid(cfg.rows, cfg.cols, len(photos_sorted), reserved)
    box_cells = center_box_cells(rows, cols, cfg.center_box_h_cells, cfg.center_box_w_cells)

    usable_side = side_px - 2 * outer_margin
    if usable_side <= 0:
        raise RuntimeError("outer_margin_px too large for the chosen size.")

    # square cells sized against the max dimension to keep them square
    cell_size = usable_side // max(rows, cols)
    grid_side = cell_size * max(rows, cols)

    grid_x0 = outer_margin + (usable_side - grid_side) // 2
    grid_y0 = outer_margin + (usable_side - grid_side) // 2

    cell_w = cell_h = cell_size
    img_w = max(1, cell_w - 2 * gutter)
    img_h = max(1, cell_h - 2 * gutter)

    canvas = Image.new("RGB", (side_px, side_px), "white")

    idx = 0
    for r in range(rows):
        for c in range(cols):
            if in_center_box(r, c, box_cells):
                continue
            if idx >= len(photos_sorted):
                break

            x = grid_x0 + c * cell_w
            y = grid_y0 + r * cell_h

            p = photos_sorted[idx]
            idx += 1

            try:
                with Image.open(p) as im:
                    im2 = fit_center_crop(im, img_w, img_h)
                    canvas.paste(im2, (x + cfg.gutter_px, y + cfg.gutter_px))
            except Exception as e:
                print(f"WARNING: failed to process {p}: {e}")

        if idx >= len(photos_sorted):
            break

    # Center title box pixel coords
    r0, c0, r1, c1 = box_cells
    box_x0 = grid_x0 + c0 * cell_w
    box_y0 = grid_y0 + r0 * cell_h
    box_x1 = grid_x0 + c1 * cell_w
    box_y1 = grid_y0 + r1 * cell_h

    draw_center_text(
        canvas=canvas,
        box_px=(box_x0, box_y0, box_x1, box_y1),
        title=cfg.title,
        subtitle=cfg.subtitle,
        font_path=cfg.font_path,
        title_size=int(cfg.title_size * cfg.preview_scale),
        subtitle_size=int(cfg.subtitle_size * cfg.preview_scale),
        title_color=cfg.title_color,
        subtitle_color=cfg.subtitle_color,
        box_bg=cfg.box_bg,
        padding_px=text_padding,
    )

    cfg.out_path.parent.mkdir(parents=True, exist_ok=True)
    ext = cfg.out_path.suffix.lower()

    if ext in {".tif", ".tiff"}:
        canvas.save(cfg.out_path, compression="tiff_deflate")
    elif ext == ".png":
        canvas.save(cfg.out_path, optimize=True)
    elif ext in {".jpg", ".jpeg"}:
        canvas.save(cfg.out_path, quality=95, subsampling=0)
    else:
        raise RuntimeError("Output must be .tif/.tiff, .png, or .jpg/.jpeg")

    print(f"Saved: {cfg.out_path}")
    print(f"Canvas: {canvas.size[0]} x {canvas.size[1]} px | Grid: {rows}x{cols} | Used: {min(idx, len(photos_sorted))}/{len(photos_sorted)}")