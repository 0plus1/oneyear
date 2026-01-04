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

## Usage

The tool generates a **square, print-quality mega-poster collage** from a folder of photos (including **HEIC**), sorted by EXIF date and arranged in a grid with white gutters and a configurable center title box.

### Basic command

```bash
uv run python main.py \
  --input "./in" \
  --output "./out/megaposter.tif"
```

---

### Required arguments

- `--input`  
  Folder containing source images. Scanned recursively.  
  Supported formats: JPG, JPEG, PNG, TIFF, WEBP, **HEIC / HEIF**.

- `--output`  
  Output file path. The file extension determines the format:  
  `.tif` / `.tiff` (recommended for print), `.png`, `.jpg`.

---

### Canvas & print settings

- `--dpi` (default: `300`)  
  Target DPI used to convert millimeters to pixels.

- `--square-mm` (default: `841`)  
  Size of the square canvas in millimeters.  
  `841` corresponds to the **short side of A0**, allowing the square to be cut from an A0 sheet.  
  Use `1189` for an A0 long-side square (significantly larger).

- `--preview-scale` (default: `1.0`)  
  Scales the entire render for faster previews without changing layout.  
  Typical preview values: `0.1` – `0.2`.

---

### Grid & layout

- `--rows` (default: auto)  
  Number of grid rows. If omitted, chosen automatically.

- `--cols` (default: auto)  
  Number of grid columns. If omitted, chosen automatically.

- `--gutter` (default: `10`)  
  White gutter in pixels around each photo inside its grid cell.

- `--outer-margin` (default: `80`)  
  White margin in pixels around the entire grid.

---

### Center title box

The center title box occupies a rectangular area measured in **grid cells**, reserved in the middle of the layout.

- `--center-box-h` (default: `5`)  
  Height of the center box in grid cells.

- `--center-box-w` (default: `7`)  
  Width of the center box in grid cells.

- `--box-bg` (default: `white`)  
  Background color of the center box.

- `--text-padding` (default: `80`)  
  Padding in pixels inside the center box.

---

### Text & typography

- `--title` (default: `"2025"`)  
  Main title text rendered in the center box.

- `--subtitle` (default: `"A year in photos"`)  
  Subtitle text rendered below the title.

- `--font` (default: system font)  
  Path to a `.ttf` font file. If omitted, a system font is used.

- `--title-size` (default: `220`)  
  Font size in pixels for the title at full resolution.

- `--subtitle-size` (default: `90`)  
  Font size in pixels for the subtitle at full resolution.

- `--title-color` (default: `#111111`)  
  Color of the title text.

- `--subtitle-color` (default: `#333333`)  
  Color of the subtitle text.

Font sizes and padding are automatically scaled when using `--preview-scale`.

---

### Examples

#### Fast preview (recommended while tuning layout)

```bash
uv run python main.py \
  --input "./in" \
  --output "./out/preview.png" \
  --preview-scale 0.15 \
  --title "2025" \
  --subtitle "Our year in 365 moments"
```

#### Full-resolution A0-square print master (TIFF)

```bash
uv run python main.py \
  --input "./in" \
  --output "./out/megaposter_a0square_300dpi.tif" \
  --dpi 300 \
  --square-mm 841 \
  --center-box-h 5 \
  --center-box-w 7 \
  --gutter 10 \
  --outer-margin 80
```

#### Custom font and colors

```bash
uv run python main.py \
  --input "./in" \
  --output "./out/megaposter.tif" \
  --font "./fonts/YourFont.ttf" \
  --title-color "#0B0B0B" \
  --subtitle-color "#444444"
```

---

### Notes

- Photos are sorted by **EXIF DateTimeOriginal**, then **DateTime**, with file modification time as fallback.
- Images are center-cropped to fill their grid cells (no letterboxing).
- The 7x5 default gives a perfect 365 photo grid; adjust these parameters and photo count to explore custom layouts.
- TIFF output is recommended for professional printing.
- Very large sizes (e.g. A0 long-side square at 300 DPI) may require significant RAM — use `--preview-scale` to iterate safely.

---

## TODO
- Face detection / subject-aware cropping
- CMYK workflows (most printers accept sRGB TIFF)
- Tiled rendering (quadrants) for ultra-large canvases
- Optional date labels per tile
- Optional “header band” instead of center box
- Optional randomization within each month
- “Polaroid” style borders or rounded corners
