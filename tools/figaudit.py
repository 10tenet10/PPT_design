"""Read-only audit of chart text layout. Re-executes the figure scripts with save() patched to
collect text geometry instead of writing PNGs. Reports: text-text collisions, text overflowing
its container box, and effective print font size at the report's display width."""
import sys, os, json, runpy, itertools
FIGDIR = "/home/claude/report/figs"
sys.path.insert(0, FIGDIR)
os.chdir(FIGDIR)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.text import Text
from matplotlib.patches import FancyBboxPatch, Rectangle
import common

DISPLAY_W_IN = (11906 - 2 * 1247) / 1440 * 0.97   # builder maxW
MAX_H_IN = 5.6
results = {}

def audit_save(fig, name):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    tight = fig.get_tightbbox(r)                      # inches
    w_in = tight.width + 2 * 0.06; h_in = tight.height + 2 * 0.06
    scale = DISPLAY_W_IN / w_in
    if h_in * scale > MAX_H_IN: scale = MAX_H_IN / h_in
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
    results[name] = {"scale": round(scale, 3), "min_print_pt": round(min(fs) * scale, 1) if fs else None,
                     "n_small": sum(1 for f in fs if f * scale < 6.0), "collisions": coll, "overflow": over,
                     "size_in": [round(w_in * scale, 2), round(h_in * scale, 2)]}
    plt.close(fig)

common.save = audit_save
for script in ["make_figs_a.py", "make_figs_a_fix.py", "make_figs_b.py", "make_figs_c.py"]:
    sys.modules.pop("make_figs_a_fix", None)
    runpy.run_path(os.path.join(FIGDIR, script), run_name="__main__")
json.dump(results, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print("audited", len(results))
