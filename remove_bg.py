"""
Remove the studio gray background from the headshot.
Samples multiple background regions (edges + interior corners of the backdrop)
and uses a larger per-pixel tolerance to handle the vignette falloff.
"""
from PIL import Image, ImageFilter
import numpy as np
from collections import deque

SRC  = "Reference Images/Joe Sargent Headshot 26.JPG"
DEST = "Reference Images/Joe Sargent Headshot 26 cutout.png"

img  = Image.open(SRC).convert("RGBA")
data = np.array(img, dtype=np.float32)
h, w = data.shape[:2]

# ── Sample background from multiple areas of the backdrop ─────────────────
# Top-center (lightest part), upper corners, and left/right mid-edge
sample_coords = [
    (20, w//2),           # top-center  (lightest)
    (20, w//4),           # top-left quarter
    (20, 3*w//4),         # top-right quarter
    (10, 10),             # corner
    (10, w-10),           # corner
    (h//3, 5),            # left edge mid
    (h//3, w-5),          # right edge mid
]
samples = [data[y, x, :3] for y, x in sample_coords]
bg = np.mean(samples, axis=0)
print(f"Background colour: rgb({int(bg[0])},{int(bg[1])},{int(bg[2])})")

# ── Global per-pixel distance mask (handles the vignette gradient) ─────────
THRESHOLD = 52   # generous — the backdrop varies ~40 units across the frame

rgb = data[:, :, :3]                         # shape (h, w, 3)
dist = np.linalg.norm(rgb - bg, axis=2)      # per-pixel distance from bg colour

# First pass: mark all pixels within threshold as candidate background
candidate = dist < THRESHOLD

# ── Flood-fill from edges to keep only CONNECTED background regions ────────
# This prevents interior areas (e.g. grey parts of clothing) from being erased
visited = np.zeros((h, w), dtype=bool)
is_bg   = np.zeros((h, w), dtype=bool)

queue = deque()
for x in range(w):
    queue.append((0, x));  queue.append((h-1, x))
for y in range(h):
    queue.append((y, 0));  queue.append((y, w-1))

while queue:
    y, x = queue.popleft()
    if y < 0 or y >= h or x < 0 or x >= w or visited[y, x]:
        continue
    visited[y, x] = True
    if candidate[y, x]:
        is_bg[y, x] = True
        queue.extend([(y+1,x),(y-1,x),(y,x+1),(y,x-1)])

# ── Soft alpha: full background → 0, soft fringe via distance ─────────────
alpha = np.where(is_bg, 0, 255).astype(np.uint8)

alpha_img = Image.fromarray(alpha, 'L')
alpha_img = alpha_img.filter(ImageFilter.MaxFilter(3))      # recover thin edges
alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(1.8)) # smooth fringe

result = img.copy()
result.putalpha(alpha_img)
result.save(DEST, "PNG")
print(f"Saved → {DEST}")
