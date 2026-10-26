"""幻灯片版作图公共层（任意行业通用）：沿用 report/figs/common.py 的风格，换成纸色调色板，直接按幻灯片尺寸出图。
作图脚本 `from deckfig import ...`；SAVE_HOOK 供 figaudit_slides.py 接管 save()。"""
import os, sys
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "report", "figs"))
import common
from common import plt, np, box, arrow, tidy
from matplotlib.text import Text

PAPER = "#F6F3EC"
plt.rcParams["figure.facecolor"] = PAPER; plt.rcParams["axes.facecolor"] = PAPER; plt.rcParams["savefig.facecolor"] = PAPER
plt.rcParams["grid.color"] = "#DAD5CA"; plt.rcParams["axes.edgecolor"] = "#8E8A80"
for i, c in enumerate(["#244B74", "#B9462B", "#2E7D5B", "#C9A227", "#C76E8C", "#3C6E3C", "#5B4FB0", "#A33A2B"]):
    common.C[i] = c
C = common.C
TXT, TXT2, MUTED, LIGHT = common.TXT, "#5A5F66", "#8A867C", "#ECE8DF"
BLUE, WARM = C[0], C[1]
# slide-scale type: common's 8–10pt × 1.32
for k in ["font.size", "axes.titlesize", "axes.labelsize", "legend.fontsize", "xtick.labelsize", "ytick.labelsize"]:
    plt.rcParams[k] = plt.rcParams[k] * 1.32

OUT = os.environ.get("FIG_OUT", os.path.join(os.getcwd(), "figs_deck"))
os.makedirs(OUT, exist_ok=True)
SAVE_HOOK = None


def blank(w=9.1, h=3.9):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    return fig, ax


def save(fig, name):
    if SAVE_HOOK:
        return SAVE_HOOK(fig, name)
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.08, dpi=200, facecolor=PAPER)
    plt.close(fig)
    print("saved", name)


_HEAD = set("，。、；：？！）》」』”’%…—·")
_TAIL = set("（《「『“‘")


def wrap_cjk(s, n):
    """按约 n 个全角字宽换行；ASCII 记半宽；标点避头尾。"""
    lines, cur, w = [], "", 0.0
    for ch in s:
        cw = 0.55 if ord(ch) < 128 else 1.0
        if w + cw > n and cur:
            if ch in _HEAD:          # 行首禁则：把标点留在上一行
                cur += ch; lines.append(cur); cur, w = "", 0.0; continue
            if cur[-1] in _TAIL:     # 行尾禁则：开括号带到下一行
                lines.append(cur[:-1]); cur, w = cur[-1], 1.0
            else:
                lines.append(cur); cur, w = "", 0.0
        cur += ch; w += cw
    if cur:
        lines.append(cur)
    return "\n".join(lines)
