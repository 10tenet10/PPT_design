"""Generate static background layers (1920x1080 PNG) borrowed from UI design idioms."""
import numpy as np, os, math, random
from PIL import Image, ImageDraw, ImageFilter
OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080

def save(img, name):
    img.save(f"{OUT}/{name}.png", optimize=True); print(name, img.size)

# 1. dot grid on paper (+ ruler ticks at the left edge) -----------------------------------------
img = Image.new("RGB", (W, H), "#F6F3EC"); d = ImageDraw.Draw(img)
for x in range(128, W - 100, 48):
    for y in range(128, 960, 48):
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill="#D9D4C8")
# ruler ticks on left margin
for i, y in enumerate(range(128, 961, 24)):
    L = 22 if i % 4 == 0 else 10
    d.line([(64, y), (64 + L, y)], fill="#B8B2A4", width=2)
# corner crop marks
for (cx, cy, sx, sy) in [(96, 96, 1, 1), (W - 96, 96, -1, 1), (96, H - 96, 1, -1), (W - 96, H - 96, -1, -1)]:
    d.line([(cx, cy), (cx + 28 * sx, cy)], fill="#8C8577", width=2)
    d.line([(cx, cy), (cx, cy + 28 * sy)], fill="#8C8577", width=2)
save(img, "bg_dotgrid")

# 2. schematic node network on dark (Mobbin-style connector lines) ------------------------------
img = Image.new("RGB", (W, H), "#0B0D10"); d = ImageDraw.Draw(img)
random.seed(7)
# hub at right-centre, nodes around, orthogonal connectors
hub = (1380, 540)
nodes = [(1040, 300), (1040, 540), (1040, 780), (1700, 330), (1700, 540), (1700, 750), (1380, 220), (1380, 860)]
line = "#1E2630"; nodec = "#131820"; edge = "#2A3340"
# faint dot texture
for x in range(0, W, 40):
    for y in range(0, H, 40):
        d.point((x, y), fill="#161A20")
for (x, y) in nodes:
    # orthogonal: horizontal then vertical
    midx = (x + hub[0]) // 2 if x != hub[0] else x
    if x != hub[0]:
        d.line([(x, y), (midx, y)], fill=line, width=2)
        d.line([(midx, y), (midx, hub[1])], fill=line, width=2)
        d.line([(midx, hub[1]), (hub[0], hub[1])], fill=line, width=2)
    else:
        d.line([(x, y), (x, hub[1])], fill=line, width=2)
for (x, y) in nodes:
    d.rounded_rectangle([x - 44, y - 44, x + 44, y + 44], radius=14, fill=nodec, outline=edge, width=2)
d.rounded_rectangle([hub[0] - 70, hub[1] - 70, hub[0] + 70, hub[1] + 70], radius=20, fill="#E8EAEE", outline="#E8EAEE")
save(img, "bg_network")

# 3. dimmed full-bleed chart with bottom fade (Ascension-style) ---------------------------------
src = Image.open("/home/claude/report/figs_dark/fig2_3_arr.png").convert("RGB")
s = max(W / src.width, H / src.height)
src = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
src = src.crop(((src.width - W) // 2, (src.height - H) // 2, (src.width - W) // 2 + W, (src.height - H) // 2 + H))
arr = np.asarray(src).astype(np.float32)
base = np.array([11, 13, 16], dtype=np.float32)
# darken to 28% then fade to base towards the bottom and the left
yy = np.linspace(0, 1, H)[:, None, None]; xx = np.linspace(0, 1, W)[None, :, None]
k = 0.28 * (1 - np.clip((yy - 0.45) / 0.55, 0, 1)) * np.clip((xx - 0.05) / 0.5, 0.15, 1)
out = base + (arr - base) * k
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(f"{OUT}/bg_chartfade.png", optimize=True); print("bg_chartfade")

# 4. radial glow + grain on dark (mesh-gradient feel) --------------------------------------------
glow = Image.new("RGB", (W, H), "#0B0D10"); g = ImageDraw.Draw(glow)
g.ellipse([1150, -250, 2100, 650], fill="#1B2D55")
g.ellipse([-300, 600, 700, 1400], fill="#17231C")
glow = glow.filter(ImageFilter.GaussianBlur(180))
a = np.asarray(glow).astype(np.float32)
rng = np.random.default_rng(3)
noise = rng.normal(0, 6, (H, W, 1))
a = np.clip(a + noise, 0, 255).astype(np.uint8)
Image.fromarray(a).save(f"{OUT}/bg_glow.png", optimize=True); print("bg_glow")

# 5. fine blueprint grid on dark olive (for the warm direction) ---------------------------------
img = Image.new("RGB", (W, H), "#3F4A2E"); d = ImageDraw.Draw(img)
for x in range(0, W, 64):
    d.line([(x, 0), (x, H)], fill="#475435", width=1)
for y in range(0, H, 64):
    d.line([(0, y), (W, y)], fill="#475435", width=1)
for x in range(0, W, 320):
    d.line([(x, 0), (x, H)], fill="#55643F", width=1)
for y in range(0, H, 320):
    d.line([(0, y), (W, y)], fill="#55643F", width=1)
save(img, "bg_blueprint")
