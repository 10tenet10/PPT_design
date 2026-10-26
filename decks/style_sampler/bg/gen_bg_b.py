"""B 海报方向的底图：暖纸点阵（E1）与压暗走势线（E3，墨黑底 + 米色线）。"""
import sys, numpy as np
from PIL import Image, ImageDraw
REPO, OUT = sys.argv[1], sys.argv[2]
W, H = 1920, 1080

# E1: dot grid + ruler ticks + crop marks on #F2EFE6
img = Image.new("RGB", (W, H), "#F2EFE6"); d = ImageDraw.Draw(img)
for x in range(128, W - 100, 48):
    for y in range(128, 960, 48):
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill="#D6D0C2")
for i, y in enumerate(range(128, 961, 24)):
    L = 22 if i % 4 == 0 else 10
    d.line([(64, y), (64 + L, y)], fill="#ADA696", width=2)
for (cx, cy, sx, sy) in [(96, 96, 1, 1), (W - 96, 96, -1, 1), (96, H - 96, 1, -1), (W - 96, H - 96, -1, -1)]:
    d.line([(cx, cy), (cx + 28 * sx, cy)], fill="#111111", width=3)
    d.line([(cx, cy), (cx, cy + 28 * sy)], fill="#111111", width=3)
img.save(f"{OUT}/bg_dotgrid_b.png", optimize=True)

# E3: chart traces with no text/axes, cream on #111111, then dimmed and faded to bottom/left
import datetime as dt, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as mdates
CREAM, INK = "#F2EFE6", "#111111"

def canvas():
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor=INK)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=INK); ax.axis("off"); return fig, ax

def fade(fig, out_name, k0):
    fig.canvas.draw(); a = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.float32); plt.close(fig)
    base = np.array([17, 17, 17], np.float32)
    yy = np.linspace(0, 1, H)[:, None, None]; xx = np.linspace(0, 1, W)[None, :, None]
    # 文字落在左下：向下、向左淡出，左下象限几乎压到底色
    k = k0 * (1 - np.clip((yy - 0.35) / 0.4, 0, 1)) * np.clip((xx - 0.25) / 0.45, 0.05, 1)
    Image.fromarray(np.clip(base + (a - base) * k, 0, 255).astype(np.uint8)).save(f"{OUT}/{out_name}", optimize=True)

# ARR trajectories (same points as report/figs/make_figs_a.py fig2_3), log scale
d = dt.date.fromisoformat
series = [
 [("2025-01-15", 0.1), ("2025-03-15", 0.2), ("2025-06-05", 0.5), ("2025-11-13", 1.0), ("2026-02-15", 2.0), ("2026-05-21", 3.0), ("2026-06-09", 4.0)],
 [("2025-10-15", 1.0), ("2026-02-12", 2.5)],
 [("2025-07-14", 0.082), ("2026-05-27", 0.492), ("2026-09-08", 0.9)],
 [("2024-12-15", 0.004), ("2025-07-15", 0.1), ("2025-12-01", 0.2), ("2026-02-15", 0.4), ("2026-06-09", 0.5), ("2026-08-31", 0.6)],
 [("2025-06-15", 0.1), ("2025-12-15", 0.265), ("2026-04-15", 0.525)],
]
fig, ax = canvas()
for i, pts in enumerate(series):
    ax.plot([d(a) for a, b in pts], [b for a, b in pts], "-o", color=CREAM, lw=5 if i == 0 else 3, ms=11 if i == 0 else 8, alpha=1 if i == 0 else 0.7)
ax.set_yscale("log"); ax.set_ylim(0.00004, 60); ax.set_xlim(d("2024-03-01"), d("2026-12-15"))
for y in (0.01, 0.1, 1):
    ax.axhline(y, color=CREAM, lw=1, alpha=0.25)
fade(fig, "bg_fade_arr_b.png", 0.34)

# bottom-up stacked bar vs institutional estimates (fig2_bottomup values), bars only
fig, ax = canvas()
comp = [40.0, 25.0, 9.0, 6.0, 5.25, 2.0]; b = 0
for i, v in enumerate(comp):
    ax.bar(1, v, bottom=b, width=0.55, color=CREAM, alpha=0.95 - i * 0.12, edgecolor=INK, linewidth=4); b += v
for x, v in [(2.2, 81.4), (3.1, 0.503), (3.9, 0.259)]:
    ax.bar(x, v, width=0.55, color=CREAM, alpha=0.55)
ax.axhline(0, color=CREAM, lw=2, alpha=0.6); ax.set_xlim(0.2, 4.6); ax.set_ylim(-4, 100)
fade(fig, "bg_fade_bars_b.png", 0.26)
print("ok")

# E3: SWE-bench Verified top score trace (same points as report/figs/make_figs_a_fix.py fig3_3), linear scale
swe = [("2024-06", 33.4), ("2024-08", 33.2), ("2024-10", 49.0), ("2025-02", 62.3), ("2025-09", 77.2), ("2025-11", 80.9),
       ("2026-02", 80.8), ("2026-04", 88.7), ("2026-05", 88.6), ("2026-06", 95.0)]
fig, ax = canvas()
ax.plot([d(a + "-15") for a, _ in swe], [b for _, b in swe], "-o", color=CREAM, lw=5, ms=11)
ax.plot([d("2025-09-15"), d("2026-05-15")], [23.3, 77.8], "-s", color=CREAM, lw=3, ms=8, alpha=0.6)
ax.set_xlim(d("2023-09-01"), d("2026-10-01")); ax.set_ylim(-110, 135)
for y in (50, 75):
    ax.axhline(y, color=CREAM, lw=1, alpha=0.25)
fade(fig, "bg_fade_swe_b.png", 0.34)

# E2: node network on paper (Mobbin-style connectors), node coordinates as background-layers.md
img = Image.new("RGB", (W, H), "#F2EFE6"); dr = ImageDraw.Draw(img)
for x in range(0, W, 40):
    for y in range(0, H, 40):
        dr.point((x, y), fill="#E2DDD0")
hub = (1380, 540)
nodes = [(1040, 300), (1040, 540), (1040, 780), (1700, 330), (1700, 540), (1700, 750), (1380, 220), (1380, 860)]
for (x, y) in nodes:
    if x != hub[0]:
        mx = (x + hub[0]) // 2
        dr.line([(x, y), (mx, y)], fill="#D6D0C2", width=3); dr.line([(mx, y), (mx, hub[1])], fill="#D6D0C2", width=3)
        dr.line([(mx, hub[1]), hub], fill="#D6D0C2", width=3)
    else:
        dr.line([(x, y), (x, hub[1])], fill="#D6D0C2", width=3)
for (x, y) in nodes:
    dr.rectangle([x - 40, y - 40, x + 40, y + 40], fill="#ECE8DD", outline="#CFC8B8", width=3)
dr.rectangle([hub[0] - 66, hub[1] - 66, hub[0] + 66, hub[1] + 66], fill="#E3DED0", outline="#B9B2A2", width=4)
img.save(f"{OUT}/bg_network_b.png", optimize=True)
print("ok2")
