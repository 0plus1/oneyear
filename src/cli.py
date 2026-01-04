import argparse
from pathlib import Path

from .config import Config, A0_SHORT_MM, A0_LONG_MM
from .render import render

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="A0-square mega-poster collage generator (EXIF-sorted, center title box, white gutters).")
    p.add_argument("--input", required=True, help="Input folder containing images (HEIC supported)")
    p.add_argument("--output", required=True, help="Output file (.tif/.png/.jpg)")

    p.add_argument("--dpi", type=int, default=300)
    p.add_argument("--square-mm", type=float, default=A0_SHORT_MM,
                   help=f"Square side in mm (default A0 short side {A0_SHORT_MM}mm; A0 long side is {A0_LONG_MM}mm)")

    p.add_argument("--gutter", type=int, default=10)
    p.add_argument("--outer-margin", type=int, default=80)

    p.add_argument("--rows", type=int, default=None)
    p.add_argument("--cols", type=int, default=None)

    p.add_argument("--center-box-h", type=int, default=5)
    p.add_argument("--center-box-w", type=int, default=7)

    p.add_argument("--title", default="2025")
    p.add_argument("--subtitle", default="A year in photos")

    p.add_argument("--font", default=None)
    p.add_argument("--title-size", type=int, default=220)
    p.add_argument("--subtitle-size", type=int, default=90)
    p.add_argument("--title-color", default="#111111")
    p.add_argument("--subtitle-color", default="#333333")
    p.add_argument("--box-bg", default="white")
    p.add_argument("--text-padding", type=int, default=80)

    p.add_argument("--preview-scale", type=float, default=1.0,
                   help="Scale down output for fast preview, e.g. 0.15")
    return p

def main() -> None:
    args = build_parser().parse_args()

    cfg = Config(
        input_dir=Path(args.input),
        out_path=Path(args.output),
        dpi=args.dpi,
        square_mm=args.square_mm,
        gutter_px=args.gutter,
        outer_margin_px=args.outer_margin,
        rows=args.rows,
        cols=args.cols,
        center_box_h_cells=args.center_box_h,
        center_box_w_cells=args.center_box_w,
        title=args.title,
        subtitle=args.subtitle,
        font_path=args.font,
        title_size=args.title_size,
        subtitle_size=args.subtitle_size,
        title_color=args.title_color,
        subtitle_color=args.subtitle_color,
        box_bg=args.box_bg,
        text_padding_px=args.text_padding,
        preview_scale=args.preview_scale,
    )

    render(cfg)

if __name__ == "__main__":
    main()
