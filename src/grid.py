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