// 把 Slides 工件的源文件（deck.json + slides/*.html）导出成不依赖 Claude 的文件：
//   <out>.pdf      ：浏览器打印，一页一张幻灯片（1920×1080），文字为矢量、可选中
//   <out>_png/     ：每页 2× 截图（3840×2160），供 pptx_from_png.py 拼成 PPTX
//   <out>_notes.json：每页讲稿（<aside>）
// 用法：node tools/render/export_deck.js <deck 的 project 目录> <blobmap> <输出路径前缀>
// 字体：Google 字体换成本地 Noto CJK / DejaVu Sans Mono（与 render_deck.js 相同）。
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const [DECK, MAP, PREFIX] = process.argv.slice(2);
const OUT = path.resolve(PREFIX); const PNG = OUT + '_png'; fs.mkdirSync(PNG, { recursive: true });
const blobs = MAP.endsWith('.json') ? JSON.parse(fs.readFileSync(MAP)) :
  Object.fromEntries(fs.readFileSync(MAP, 'utf8').split('\n').filter(l => l.trim()).map(l => { const [k, v] = l.trim().split(/\s+/); return [k, path.resolve(v)]; }));
const order = JSON.parse(fs.readFileSync(`${DECK}/deck.json`)).order;
const CSS = `<style>@page{size:1920px 1080px;margin:0}html,body{margin:0;background:#fff}
section{position:relative;width:1920px;height:1080px;overflow:hidden;box-sizing:border-box;break-after:page}
section *{box-sizing:border-box;margin:0}ul,ol{padding-left:1.2em}table{border-collapse:collapse}td,th{border:1px solid #c9c8c2;padding:.35em .6em;vertical-align:top;text-align:left}
aside{display:none}img{display:block}div:not([style*="display"]){display:flex;flex-direction:column}div[style*="display:flex"]:not([style*="flex-direction"]){flex-direction:row}
*{-webkit-print-color-adjust:exact;print-color-adjust:exact}</style>`;
const fix = h => h.replace(/\/_blob\/([0-9a-f]{32})/g, (m, id) => {
    if (!blobs[id]) throw new Error('no local file for blob ' + id); return 'file://' + blobs[id]; })
  .replaceAll("'Noto Sans SC'", "'Noto Sans CJK SC'").replaceAll("'Noto Serif SC'", "'Noto Serif CJK SC'")
  .replaceAll("'JetBrains Mono'", "'DejaVu Sans Mono'").replaceAll("'IBM Plex Mono'", "'DejaVu Sans Mono'");
(async () => {
  const slides = order.map(sid => fs.readFileSync(`${DECK}/slides/${sid}.html`, 'utf8'));
  const notes = slides.map(h => { const m = h.match(/<aside>([\s\S]*?)<\/aside>/); return m ? m[1].trim() : ''; });
  fs.writeFileSync(OUT + '_notes.json', JSON.stringify(order.map((id, i) => ({ id, notes: notes[i] })), null, 1));
  const tmp = OUT + '_all.html';
  fs.writeFileSync(tmp, `<!doctype html><html><head><meta charset=utf-8>${CSS}</head><body>${slides.map(fix).join('\n')}</body></html>`);
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await pg.goto('file://' + tmp, { waitUntil: 'load' }); await pg.waitForTimeout(500);
  await pg.pdf({ path: OUT + '.pdf', width: '1920px', height: '1080px', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  const shot = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  for (const [i, h] of slides.entries()) {
    const one = OUT + '_one.html';
    fs.writeFileSync(one, `<!doctype html><html><head><meta charset=utf-8>${CSS}</head><body>${fix(h)}</body></html>`);
    await shot.goto('file://' + one, { waitUntil: 'load' }); await shot.waitForTimeout(100);
    await shot.screenshot({ path: path.join(PNG, `${String(i + 1).padStart(2, '0')}.png`), clip: { x: 0, y: 0, width: 1920, height: 1080 } });
    fs.unlinkSync(one);
  }
  fs.unlinkSync(tmp); await b.close();
  console.log(`exported ${order.length} slides → ${OUT}.pdf, ${PNG}/`);
})();
