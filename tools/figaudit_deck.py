import sys, os, json, runpy, itertools
FIGDIR="/home/claude/report/figs"; sys.path.insert(0, FIGDIR); os.chdir(FIGDIR)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.text import Text
from matplotlib.patches import FancyBboxPatch, Rectangle
import common
PAPER="#F6F3EC"
plt.rcParams["figure.facecolor"]=PAPER; plt.rcParams["axes.facecolor"]=PAPER; plt.rcParams["savefig.facecolor"]=PAPER
plt.rcParams["grid.color"]="#DAD5CA"; plt.rcParams["axes.edgecolor"]="#8E8A80"
for i,c in enumerate(["#244B74","#B9462B","#2E7D5B","#C9A227","#C76E8C","#3C6E3C","#5B4FB0","#A33A2B"]): common.C[i]=c
common.LIGHT="#ECE8DF"; common.MUTED="#8A867C"; common.TXT2="#5A5F66"
import json; CFG=json.load(open("/tmp/claude-0/-home-claude/e9602583-6fd0-5070-905f-0a76d9c21e58/scratchpad/deck_cfg.json")); KW,KH0,KF=CFG["default"]
_os=plt.subplots
def subplots(*a,**k):
    fs=k.get("figsize")
    if fs: pass
    return _os(*a,**k)
plt.subplots=subplots
def blank(w=6.3,h=3.6):
    fig,ax=_os(figsize=(w,h)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off"); return fig,ax
common.blank=blank
SLIDE_IN=13.333; BOX_W=1664/1920*SLIDE_IN; BOX_H=640/1080*7.5
results={}
def audit_save(fig,name):
    kw,kh,kf=CFG.get(name,CFG["default"])
    w0,h0=fig.get_size_inches(); fig.set_size_inches(w0*kw,h0*kh)
    for t in fig.findobj(Text):
        try: t.set_fontsize(t.get_fontsize()*kf)
        except Exception: pass
    fig.canvas.draw(); r=fig.canvas.get_renderer(); tight=fig.get_tightbbox(r)
    w_in=tight.width+0.16; h_in=tight.height+0.16
    scale=min(BOX_W/w_in, BOX_H/h_in)
    texts=[]
    for t in fig.findobj(Text):
        if not t.get_visible() or not t.get_text().strip(): continue
        try: bb=t.get_window_extent(r)
        except Exception: continue
        if bb.width<1 or bb.height<1: continue
        texts.append((t.get_text().replace("\n","⏎")[:40],bb,t.get_fontsize()))
    coll=[]
    for (a,ba,_),(b,bb_,_) in itertools.combinations(texts,2):
        ix=min(ba.x1,bb_.x1)-max(ba.x0,bb_.x0); iy=min(ba.y1,bb_.y1)-max(ba.y0,bb_.y0)
        if ix>1 and iy>1:
            inter=ix*iy; small=min(ba.width*ba.height,bb_.width*bb_.height)
            if inter/small>0.08: coll.append((a,b,round(inter/small,2)))
    over=[]; boxes=[]
    for ax in fig.axes:
        axbb=ax.get_window_extent(r)
        for p in ax.patches:
            if isinstance(p,(FancyBboxPatch,Rectangle)) and p is not ax.patch:
                bb=p.get_window_extent(r)
                if bb.width*bb.height<0.6*axbb.width*axbb.height and bb.width>8 and bb.height>8: boxes.append(bb)
    for (s,tb,_) in texts:
        cx,cy=(tb.x0+tb.x1)/2,(tb.y0+tb.y1)/2
        inside=[b for b in boxes if b.x0<=cx<=b.x1 and b.y0<=cy<=b.y1]
        if not inside: continue
        b=min(inside,key=lambda z:z.width*z.height)
        dx=max(b.x0-tb.x0,tb.x1-b.x1,0); dy=max(b.y0-tb.y0,tb.y1-b.y1,0)
        if dx>2 or dy>2: over.append((s,round(dx,1),round(dy,1)))
    fs=[f for _,_,f in texts]
    results[name]={"min_proj_pt":round(min(fs)*scale,1) if fs else None,"collisions":coll,"overflow":over,"size_in":[round(w_in*scale,2),round(h_in*scale,2)]}
    plt.close(fig)
common.save=audit_save
for s in ["make_figs_a.py","make_figs_a_fix.py","make_figs_b.py","make_figs_c.py"]:
    sys.modules.pop("make_figs_a_fix",None); runpy.run_path(os.path.join(FIGDIR,s),run_name="__main__")
json.dump(results,open(sys.argv[1],"w"),ensure_ascii=False,indent=1)
