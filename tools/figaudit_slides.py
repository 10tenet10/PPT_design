"""figaudit.py 的通用幻灯片版：重跑 make_figs.py，把 save() 换成测量；按 1664×580 contain 版面换算成幻灯片像素字号。
用法：python3 tools/figaudit_slides.py <make_figs.py> <out.json>"""
import sys, os, json, runpy, itertools
SCRIPT, OUTJ = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(SCRIPT)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.text import Text
from matplotlib.patches import FancyBboxPatch, Rectangle
import deckfig

BOX_W, BOX_H, DPI = 1664, 580, 200
results = {}

def audit_save(fig, name):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    tight = fig.get_tightbbox(r)
    w_in = tight.width + 2 * 0.08; h_in = tight.height + 2 * 0.08
    scale = min(BOX_W / (w_in * DPI), BOX_H / (h_in * DPI))
    texts = []
    for t in fig.findobj(Text):
        if not t.get_visible() or not t.get_text().strip(): continue
        try: bb = t.get_window_extent(r)
        except Exception: continue
        if bb.width < 1 or bb.height < 1: continue
        texts.append((t.get_text().replace("\n", "⏎")[:40], bb, t.get_fontsize()))
    # collisions
    coll = []
    for (a, ba, _), (b, bb_, _) in itertools.combinations(texts, 2):
        ix = min(ba.x1, bb_.x1) - max(ba.x0, bb_.x0); iy = min(ba.y1, bb_.y1) - max(ba.y0, bb_.y0)
        if ix > 1 and iy > 1:
            inter = ix * iy; small = min(ba.width * ba.height, bb_.width * bb_.height)
            if inter / small > 0.08: coll.append((a, b, round(inter / small, 2)))
    # overflow from container boxes (patches drawn in axes, not full-axes backgrounds)
    over = []
    boxes = []
    for ax in fig.axes:
        for p in ax.patches:
            if isinstance(p, (FancyBboxPatch, Rectangle)) and p is not ax.patch:
                bb = p.get_window_extent(r)
                axbb = ax.get_window_extent(r)
                if bb.width * bb.height < 0.6 * axbb.width * axbb.height and bb.width > 8 and bb.height > 8:
                    boxes.append(bb)
    for (s, tb, _) in texts:
        cx, cy = (tb.x0 + tb.x1) / 2, (tb.y0 + tb.y1) / 2
        inside = [b for b in boxes if b.x0 <= cx <= b.x1 and b.y0 <= cy <= b.y1]
        if not inside: continue
        b = min(inside, key=lambda z: z.width * z.height)
        dx = max(b.x0 - tb.x0, tb.x1 - b.x1, 0); dy = max(b.y0 - tb.y0, tb.y1 - b.y1, 0)
        if dx > 2 or dy > 2: over.append((s, round(dx, 1), round(dy, 1)))
    fs = [f for _, _, f in texts]
    px = lambda f: f / 72 * DPI * scale
    results[name] = {"scale": round(scale, 3), "min_slide_px": round(px(min(fs)), 1) if fs else None,
                     "n_small": sum(1 for f in fs if px(f) < 18), "collisions": coll, "overflow": over,
                     "shown_px": [round(w_in * DPI * scale), round(h_in * DPI * scale)]}
    plt.close(fig)

deckfig.SAVE_HOOK = audit_save
runpy.run_path(SCRIPT, run_name="__main__")
json.dump(results, open(OUTJ, "w"), ensure_ascii=False, indent=1)
print("audited", len(results))
