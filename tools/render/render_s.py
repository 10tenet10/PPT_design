"""Render each slide file as a 1920x1080 page and report layout problems (flow content reaching the footer band,
elements past the canvas, overflowing text). Read-only on the deck files."""
import re, glob, json, os, sys, asyncio
from playwright.async_api import async_playwright
SP="/tmp/claude-0/-home-claude/e9602583-6fd0-5070-905f-0a76d9c21e58/scratchpad"
DECK=f"{SP}/styles/project"; OUT=f"{SP}/render/shots_s"; os.makedirs(OUT,exist_ok=True)
blobs={}
for line in open(f"{SP}/render/blobmap.txt"):
    k,v=line.split(); blobs[k]=v
order=json.load(open(f"{DECK}/deck.json"))["order"]
CSS="""<style>html,body{margin:0;background:#888}section{position:relative;width:1920px;height:1080px;overflow:hidden;box-sizing:border-box}
section *{box-sizing:border-box;margin:0}h1,h2,h3,p,ul,ol{margin:0}ul,ol{padding-left:1.2em}table{border-collapse:collapse}td,th{border:1px solid #c9c8c2;padding:.35em .6em;vertical-align:top;text-align:left}
aside{display:none}img{display:block}div:not([style*="display"]){display:flex;flex-direction:column}div[style*="display:flex"]:not([style*="flex-direction"]){flex-direction:row}</style>"""
JS="""() => {const sec=document.querySelector('section'); const r=sec.getBoundingClientRect();
const pinned=[...sec.children].filter(e=>getComputedStyle(e).position==='absolute');
const flow=[...sec.children].filter(e=>getComputedStyle(e).position!=='absolute' && e.tagName!=='ASIDE');
let footTop=1080; for(const p of pinned){const b=p.getBoundingClientRect(); if(b.top>900) footTop=Math.min(footTop,b.top);}
let flowBottom=0; for(const f of flow){flowBottom=Math.max(flowBottom,f.getBoundingClientRect().bottom);}
const over=[]; for(const e of sec.querySelectorAll('*')){if(e.tagName==='ASIDE')continue; const b=e.getBoundingClientRect(); if(b.right>1921||b.bottom>1081) over.push(e.tagName+':'+(e.textContent||'').slice(0,20));
 if(e.scrollWidth>e.clientWidth+2 && getComputedStyle(e).overflow!=='visible') over.push('scroll:'+e.tagName);}
const titles=[...sec.querySelectorAll('h2')].map(h=>{const b=h.getBoundingClientRect();return {lines:Math.round(b.height/(parseFloat(getComputedStyle(h).lineHeight)))}});
return {flowBottom:Math.round(flowBottom), footTop:Math.round(footTop), over, titleLines:titles.map(t=>t.lines)};}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":1920,"height":1080})
        report={}
        for sid in order:
            if not os.path.exists(f"{DECK}/slides/{sid}.html"): continue
            html=open(f"{DECK}/slides/{sid}.html",encoding="utf8").read()
            html=re.sub(r'/_blob/([0-9a-f]{32})', lambda m: "file://"+blobs.get(m.group(1),"/nonexistent"), html)
            html=html.replace("'Noto Sans SC'","'Noto Sans CJK SC'").replace("'Noto Serif SC'","'Noto Serif CJK SC'").replace("'IBM Plex Mono'","'DejaVu Sans Mono'").replace("'JetBrains Mono'","'DejaVu Sans Mono'").replace("'Space Grotesk'","'DejaVu Sans'")
            tmp=f"{SP}/render/tmp_{sid}.html"; open(tmp,"w",encoding="utf8").write("<!doctype html><html><head><meta charset=utf-8>"+CSS+"</head><body>"+html+"</body></html>")
            await pg.goto("file://"+tmp)
            await pg.wait_for_timeout(150)
            info=await pg.evaluate(JS)
            await pg.screenshot(path=f"{OUT}/{order.index(sid):02d}-{sid}.png", clip={"x":0,"y":0,"width":1920,"height":1080}, scale="css")
            report[sid]=info
        await b.close()
    json.dump(report,open(f"{SP}/render/report_s.json","w"),ensure_ascii=False,indent=1)
    for sid,i in report.items():
        flag=[]
        if i["flowBottom"]>i["footTop"]-8: flag.append(f"flow {i['flowBottom']} reaches footer {i['footTop']}")
        if i["over"]: flag.append("over:"+";".join(i["over"][:3]))
        if any(t>2 for t in i["titleLines"]): flag.append(f"title {i['titleLines']} lines")
        print(f"{sid:18s} bottom={i['flowBottom']:4d} foot={i['footTop']:4d} {' | '.join(flag)}")
asyncio.run(main())
