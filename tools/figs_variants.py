"""Figure variants for style samples: dark (A) and monochrome (C). Writes to figs_dark/ and figs_mono/."""
import sys, os, runpy, json
VAR=sys.argv[1]; FIGDIR="/home/claude/report/figs"; OUT=f"/home/claude/report/figs_{VAR}/"; os.makedirs(OUT,exist_ok=True)
sys.path.insert(0,FIGDIR); os.chdir(FIGDIR)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.text import Text
import common
if VAR=="dark":
    BG="#0B0D10"; FG="#E8EAEE"; GRID="#23272E"; PAL=["#7AA2FF","#FF8A5B","#4FD1A5","#F5C84B","#D08BE0","#7CCB6F","#9B8CFF","#FF6B6B"]
    common.TXT="#E8EAEE"; common.TXT2="#AEB4BE"; common.MUTED="#7B8290"; common.LIGHT="#161A20"
else:
    BG="#FFFFFF"; FG="#111111"; GRID="#E6E6E6"; PAL=["#111111","#8A8A8A","#C4C4C4","#555555","#A0A0A0","#333333","#707070","#111111"]
    common.TXT="#111111"; common.TXT2="#555555"; common.MUTED="#8A8A8A"; common.LIGHT="#F2F2F2"
for i,c in enumerate(PAL): common.C[i]=c
plt.rcParams.update({"figure.facecolor":BG,"axes.facecolor":BG,"savefig.facecolor":BG,"text.color":FG,"axes.labelcolor":FG,"xtick.color":FG,"ytick.color":FG,"axes.edgecolor":GRID if VAR=="dark" else "#999","grid.color":GRID})
CFG=json.load(open("/tmp/claude-0/-home-claude/e9602583-6fd0-5070-905f-0a76d9c21e58/scratchpad/deck_cfg.json"))
WANT={"fig2_3_arr.png","fig7_2_usage.png","fig6_4_horizon.png","fig2_bottomup.png"}
def save(fig,name):
    if name not in WANT: plt.close(fig); return
    kw,kh,kf=CFG.get(name,CFG["default"]); w0,h0=fig.get_size_inches(); fig.set_size_inches(w0*kw,h0*kh)
    for t in fig.findobj(Text):
        try: t.set_fontsize(t.get_fontsize()*kf)
        except Exception: pass
        if VAR=="dark" and t.get_color() in ("#0b0b0b","#52514e","#8a8984","#14365F","#3D3D3A","#2E2E2C","k","black"): t.set_color(FG)
    for ax in fig.axes:
        for ln in ax.get_lines(): ln.set_linewidth(ln.get_linewidth()*1.25); ln.set_markersize(ln.get_markersize()*1.2)
        if VAR=="dark":
            for sp in ax.spines.values(): sp.set_color(GRID)
            ax.tick_params(colors=FG); 
            for t in ax.get_xticklabels()+ax.get_yticklabels(): t.set_color(FG)
    fig.savefig(OUT+name,bbox_inches="tight",pad_inches=0.08,dpi=200,facecolor=BG); plt.close(fig)
common.save=save
for s in ["make_figs_a.py","make_figs_a_fix.py","make_figs_b.py","make_figs_c.py"]:
    sys.modules.pop("make_figs_a_fix",None); runpy.run_path(os.path.join(FIGDIR,s),run_name="__main__")
print(VAR,"done")
