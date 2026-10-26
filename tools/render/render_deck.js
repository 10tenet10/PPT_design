// 通用幻灯片渲染自查（任意 deck）：每页 1920×1080 截图，并报告正文触底、越界、固定文字框重叠、标题行数。
// 用法：node tools/render/render_deck.js <deck 的 project 目录> <blobmap> <输出目录>
//   blobmap：.json（{"<blob id>": "本地 PNG 路径"}）或 .txt（每行 "<blob id> <本地路径>"）；相对路径按当前目录解析。
//   依赖 Node 版 playwright 与本地 Chromium；字体用 Noto CJK / DejaVu Sans Mono 替代 Google 字体。
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const [DECK, MAP, OUT0] = process.argv.slice(2); const OUT = path.resolve(OUT0); fs.mkdirSync(OUT, { recursive: true });
const blobs = MAP.endsWith('.json') ? JSON.parse(fs.readFileSync(MAP)) :
  Object.fromEntries(fs.readFileSync(MAP, 'utf8').split('\n').filter(l => l.trim()).map(l => { const [k, v] = l.trim().split(/\s+/); return [k, path.resolve(v)]; })); const order = JSON.parse(fs.readFileSync(`${DECK}/deck.json`)).order;
const CSS = `<style>html,body{margin:0;background:#888}section{position:relative;width:1920px;height:1080px;overflow:hidden;box-sizing:border-box}
section *{box-sizing:border-box;margin:0}ul,ol{padding-left:1.2em}table{border-collapse:collapse}td,th{border:1px solid #c9c8c2;padding:.35em .6em;vertical-align:top;text-align:left}
aside{display:none}img{display:block}div:not([style*="display"]){display:flex;flex-direction:column}div[style*="display:flex"]:not([style*="flex-direction"]){flex-direction:row}</style>`;
const JS = () => { const sec = document.querySelector('section');
  const pinned = [...sec.children].filter(e => getComputedStyle(e).position === 'absolute');
  const flow = [...sec.children].filter(e => getComputedStyle(e).position !== 'absolute' && e.tagName !== 'ASIDE');
  let footTop = 1080; for (const p of pinned) { const b = p.getBoundingClientRect(); if (b.top > 900 && b.height < 120) footTop = Math.min(footTop, b.top); }
  let flowBottom = 0; for (const f of flow) flowBottom = Math.max(flowBottom, f.getBoundingClientRect().bottom);
  // content inside full-bleed containers
  for (const p of pinned) { const b = p.getBoundingClientRect(); if (p.tagName === 'DIV' && b.height > 500) for (const c of p.querySelectorAll('p,h1,h2,h3,table,img')) flowBottom = Math.max(flowBottom, c.getBoundingClientRect().bottom); }
  const over = []; for (const e of sec.querySelectorAll('*')) { if (e.tagName === 'ASIDE') continue; const b = e.getBoundingClientRect();
    if (b.width && (b.right > 1921 || b.bottom > 1081)) over.push(e.tagName + ':' + (e.textContent || '').slice(0, 16));
    if (/^(P|H1|H2|H3)$/.test(e.tagName) && e.scrollWidth > e.clientWidth + 2) over.push('hscroll:' + (e.textContent || '').slice(0, 16)); }
  // pinned text boxes overlapping each other
  const txt = [...sec.querySelectorAll('p')].filter(e => getComputedStyle(e).position === 'absolute').map(e => [e, e.getBoundingClientRect()]);
  const coll = []; for (let i = 0; i < txt.length; i++) for (let j = i + 1; j < txt.length; j++) { const a = txt[i][1], b = txt[j][1];
    if (a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom) coll.push(txt[i][0].textContent.slice(0, 10) + '×' + txt[j][0].textContent.slice(0, 10)); }
  const titles = [...sec.querySelectorAll('h1,h2')].map(h => Math.round(h.getBoundingClientRect().height / parseFloat(getComputedStyle(h).lineHeight)));
  return { flowBottom: Math.round(flowBottom), footTop: Math.round(footTop), over, coll, titles }; };
(async () => { const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } }); const report = {};
  for (const [i, sid] of order.entries()) {
    let html = fs.readFileSync(`${DECK}/slides/${sid}.html`, 'utf8');
    html = html.replace(/\/_blob\/([0-9a-f]{32})/g, (m, id) => 'file://' + (blobs[id] || '/nonexistent'))
      .replaceAll("'Noto Sans SC'", "'Noto Sans CJK SC'").replaceAll("'Noto Serif SC'", "'Noto Serif CJK SC'")
      .replaceAll("'JetBrains Mono'", "'DejaVu Sans Mono'").replaceAll("'IBM Plex Mono'", "'DejaVu Sans Mono'");
    const tmp = path.join(OUT, `tmp_${sid}.html`); fs.writeFileSync(tmp, `<!doctype html><html><head><meta charset=utf-8>${CSS}</head><body>${html}</body></html>`);
    await pg.goto('file://' + tmp); await pg.waitForTimeout(120);
    report[sid] = await pg.evaluate(JS);
    await pg.screenshot({ path: path.join(OUT, `${String(i + 1).padStart(2, '0')}-${sid}.png`), clip: { x: 0, y: 0, width: 1920, height: 1080 } });
    fs.unlinkSync(tmp); }
  await b.close(); fs.writeFileSync(path.join(OUT, 'report.json'), JSON.stringify(report, null, 1));
  for (const [sid, r] of Object.entries(report)) { const f = [];
    if (r.flowBottom > r.footTop - 8) f.push(`touch ${r.flowBottom}/${r.footTop}`);
    if (r.over.length) f.push('over:' + r.over.slice(0, 3).join(';'));
    if (r.coll.length) f.push('coll:' + r.coll.slice(0, 3).join(';'));
    if (r.titles.some(t => t > 2)) f.push('title ' + r.titles.join(','));
    console.log(sid.padEnd(16), String(r.flowBottom).padStart(4), String(r.footTop).padStart(4), f.join(' | ')); } })();
