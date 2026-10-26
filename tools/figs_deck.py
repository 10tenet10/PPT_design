"""Deck mode: re-run the report figure scripts with wider (16:9-leaning) canvases and larger type.
Writes PNGs to /home/claude/report/figs_deck/ ; never touches the report's own PNGs."""
import sys, os, runpy, json
FIGDIR = "/home/claude/report/figs"; OUTDIR = "/home/claude/report/figs_deck/"
os.makedirs(OUTDIR, exist_ok=True)
sys.path.insert(0, FIGDIR); os.chdir(FIGDIR)
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.text import Text
import common
PAPER="#F6F3EC"
plt.rcParams["figure.facecolor"]=PAPER; plt.rcParams["axes.facecolor"]=PAPER; plt.rcParams["savefig.facecolor"]=PAPER
plt.rcParams["grid.color"]="#DAD5CA"; plt.rcParams["axes.edgecolor"]="#8E8A80"
for i,c in enumerate(["#244B74","#B9462B","#2E7D5B","#C9A227","#C76E8C","#3C6E3C","#5B4FB0","#A33A2B"]): common.C[i]=c
common.LIGHT="#ECE8DF"; common.MUTED="#8A867C"; common.TXT2="#5A5F66"

CFG=json.load(open("/tmp/claude-0/-home-claude/e9602583-6fd0-5070-905f-0a76d9c21e58/scratchpad/deck_cfg.json")); KW,KH0,KF=CFG["default"]
_orig_subplots = plt.subplots
def subplots(*a, **k):
    fs = k.get("figsize")
    if fs: pass
    return _orig_subplots(*a, **k)
plt.subplots = subplots
def blank(w=6.3, h=3.6):
    fig, ax = _orig_subplots(figsize=(w, h))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    return fig, ax
common.blank = blank
_orig_save = common.save
def save(fig, name):
    kw, kh, kf = CFG.get(name, CFG["default"])
    w0, h0 = fig.get_size_inches(); fig.set_size_inches(w0 * kw, h0 * kh)
    for t in fig.findobj(Text):
        try: t.set_fontsize(t.get_fontsize() * kf)
        except Exception: pass
    for ax in fig.axes:
        for ln in ax.get_lines():
            ln.set_linewidth(ln.get_linewidth() * 1.25); ln.set_markersize(ln.get_markersize() * 1.2)
    fig.savefig(OUTDIR + name, bbox_inches="tight", pad_inches=0.08, dpi=200, facecolor=PAPER)
    plt.close(fig)
common.save = save
for script in ["make_figs_a.py", "make_figs_a_fix.py", "make_figs_b.py", "make_figs_c.py"]:
    sys.modules.pop("make_figs_a_fix", None)
    g = runpy.run_path(os.path.join(FIGDIR, script), run_name="__main__")
print("deck figs written")
