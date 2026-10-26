import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

for f in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
          "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
          "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"]:
    try:
        font_manager.fontManager.addfont(f)
    except Exception:
        pass

plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 9
plt.rcParams["axes.titlesize"] = 10
plt.rcParams["axes.labelsize"] = 9
plt.rcParams["legend.fontsize"] = 8
plt.rcParams["xtick.labelsize"] = 8
plt.rcParams["ytick.labelsize"] = 8
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.edgecolor"] = "#9a9a94"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["grid.color"] = "#e6e5e0"
plt.rcParams["grid.linewidth"] = 0.6
plt.rcParams["savefig.dpi"] = 220
plt.rcParams["figure.facecolor"] = "white"

# categorical palette (fixed order)
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
TXT = "#0b0b0b"; TXT2 = "#52514e"; MUTED = "#8a8984"
SEQ = ["#dbe8f8", "#b7d0f0", "#8db3e7", "#5f93dd", "#2a78d6", "#1f5aa3", "#143c6e"]
STATUS = {"good": "#1a8a3a", "warn": "#d48b00", "serious": "#d9541e", "critical": "#b3261e"}
LIGHT = "#f4f3ef"

OUT = "/home/claude/report/figs/"

def box(ax, x, y, w, h, text, fc="#ffffff", ec="#9a9a94", fs=8, lw=0.9, tc=TXT, bold=False, rounding=0.02, ha="center", va="center", zorder=3):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={rounding}",
                       fc=fc, ec=ec, lw=lw, zorder=zorder)
    ax.add_patch(p)
    if text:
        tx = x + w / 2 if ha == "center" else x + 0.012
        ax.text(tx, y + h / 2, text, ha=ha, va=va, fontsize=fs, color=tc,
                weight="bold" if bold else "normal", zorder=zorder + 1, linespacing=1.25)
    return p

def arrow(ax, x1, y1, x2, y2, color="#6f6e69", lw=1.0, style="-|>", ls="-", mutation=8, zorder=2, cs=None):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, color=color, lw=lw,
                        mutation_scale=mutation, linestyle=ls, zorder=zorder,
                        connectionstyle=cs if cs else "arc3,rad=0")
    ax.add_patch(a)
    return a

def blank(w=6.3, h=3.6):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    return fig, ax

def save(fig, name):
    fig.savefig(OUT + name, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print("saved", name)

def tidy(ax, ygrid=True):
    if ygrid:
        ax.yaxis.grid(True); ax.set_axisbelow(True)
    ax.tick_params(length=0)

# escape "$" so matplotlib does not switch to mathtext
import matplotlib.text as _mtext
_orig_set_text = _mtext.Text.set_text
def _set_text(self, s):
    if isinstance(s, str) and "$" in s and "\\$" not in s and "\\math" not in s:
        s = s.replace("$", r"\$")
    _orig_set_text(self, s)
_mtext.Text.set_text = _set_text
