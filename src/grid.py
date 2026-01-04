import math
from typing import Optional, Tuple

def mm_to_px(mm: float, dpi: int) -> int:
    inches = mm / 25.4
    return int(round(inches * dpi))

def choose_grid(n_photos: int, reserved_cells: int) -> Tuple[int, int]:
    needed = n_photos + reserved_cells
    side = int(math.ceil(math.sqrt(needed)))

    best = None
    for rows in range(max(1, side - 10), side + 11):
        for cols in range(max(1, side - 10), side + 11):
            if rows * cols >= needed:
                area = rows * cols
                aspect_penalty = abs(rows - cols)
                candidate = (aspect_penalty, area, rows, cols)
                if best is None or candidate < best:
                    best = candidate

    assert best is not None
    return best[2], best[3]

def center_box_cells(rows: int, cols: int, box_h: int, box_w: int) -> Tuple[int, int, int, int]:
    box_h = min(box_h, rows)
    box_w = min(box_w, cols)

    r0 = (rows - box_h) // 2
    c0 = (cols - box_w) // 2
    r1 = r0 + box_h
    c1 = c0 + box_w
    return r0, c0, r1, c1

def in_center_box(r: int, c: int, box: Tuple[int, int, int, int]) -> bool:
    r0, c0, r1, c1 = box
    return (r0 <= r < r1) and (c0 <= c < c1)

def resolve_grid(rows: Optional[int], cols: Optional[int], n_photos: int, reserved: int) -> Tuple[int, int]:
    if rows and cols:
        if rows * cols - reserved < n_photos:
            raise ValueError(f"Grid too small: rows*cols - reserved = {rows*cols - reserved} < {n_photos}")
        return rows, cols
    return choose_grid(n_photos, reserved)

def compute_grid_and_center_box_for_count(photo_count: int, target_ratio: float = 1.6) -> Tuple[int, int, int, int]:
    """
    Returns (rows, cols, center_box_h, center_box_w) where:
      rows = cols = N (square grid)
      center_box_h * center_box_w = N*N - photo_count   (exactly)
    We try to pick a rectangle whose aspect ratio (w/h) is close to target_ratio.
    """
    if photo_count <= 0:
        raise ValueError("photo_count must be > 0")

    N = int(math.ceil(math.sqrt(photo_count)))
    reserved = N * N - photo_count

    if reserved == 0:
        return N, N, 0, 0

    best = None
    # Find factor pairs h*w == reserved
    for h in range(1, reserved + 1):
        if reserved % h != 0:
            continue
        w = reserved // h

        # must fit inside the grid
        if h > N or w > N:
            continue

        # prefer w >= h (landscape-ish), but allow both
        aspect = (w / h) if h else 999
        score = (
            abs(aspect - target_ratio),   # primary: match nice rectangle ratio
            abs(w - h),                   # secondary: not too skinny
            -min(w, h)                    # tertiary: slightly prefer larger box
        )
        cand = (score, h, w)
        if best is None or cand < best:
            best = cand

    if best is None:
        # fallback: extremely skinny box; still guaranteed mathematically
        # but should basically never happen for normal sizes
        h, w = 1, reserved
        if w > N:
            # if it truly cannot fit, bump N by 1 (rare edge)
            N += 1
            reserved = N * N - photo_count
            return compute_grid_and_center_box_for_count(photo_count, target_ratio)

        return N, N, h, w

    _, h, w = best
    return N, N, h, w