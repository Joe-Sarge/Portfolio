"""
Crop watermark bars from Sports Innovation Forum photos
and prepare the Morehouse panel image (rotate + crop to Joe).
"""
from PIL import Image

BASE = "Reference Images/"

# ── 1. IMG_2466.JPEG — remove bottom SIF bar (~18 % of height) ───────────
img = Image.open(BASE + "IMG_2466.JPEG")
w, h = img.size
crop_h = int(h * 0.82)
img.crop((0, 0, w, crop_h)).save(BASE + "IMG_2466_c.JPEG", quality=92)
print(f"IMG_2466:  {w}×{h} → {w}×{crop_h}")

# ── 2. IMG_7553.JPEG — same treatment ────────────────────────────────────
img = Image.open(BASE + "IMG_7553.JPEG")
w, h = img.size
crop_h = int(h * 0.82)
img.crop((0, 0, w, crop_h)).save(BASE + "IMG_7553_c.JPEG", quality=92)
print(f"IMG_7553:  {w}×{h} → {w}×{crop_h}")

# ── 3. Morehouse — rotate 90 ° CCW (positive = CCW in PIL) ───────────────
img = Image.open(BASE + "Morehouse Sports Panel1879.JPG")
img = img.rotate(90, expand=True)   # CCW brings head upright
w, h = img.size
print(f"Morehouse rotated: {w}×{h}")

# After CCW rotation, Joe is roughly at (58 % x, 50 % y).
# Crop: full width, vertical window centred around 40–80 % of height.
top    = int(h * 0.10)
bottom = int(h * 0.78)
img.crop((0, top, w, bottom)).save(BASE + "Morehouse_c.JPEG", quality=92)
print(f"Morehouse crop: y {top}→{bottom}  ({w}×{bottom-top})")
