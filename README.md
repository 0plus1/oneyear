# oneyear — A0 Square Photo Collage Generator

Generate a print-quality **square** mega-poster collage (e.g. “365 photos”) with:
- EXIF-date sorting (DateTimeOriginal → DateTime → mtime fallback)
- A configurable **grid** with **white gutters** around each photo
- A configurable **center title box** (title + subtitle)
- A fast **preview mode** (scaled output) for quick iteration
- Print-friendly output (TIFF recommended)

Built in Python with Pillow. Managed **strictly with `uv`**.

## Requirements
- Python 3.10+ recommended
- [`uv`](https://github.com/astral-sh/uv)
- [`libheif`](https://github.com/strukturag/libheif) (if HEIF format is needed)

## Install
```bash
uv init
```