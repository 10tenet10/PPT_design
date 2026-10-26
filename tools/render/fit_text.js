// 动态填充：按基准字号表抬高正文字号，再以 2px 步进放大到填满可用高度；违反任一约束即停。
// 用法：node tools/render/fit_text.js <deck 的 project 目录> <blobmap> [--dry]
//   直接改写 slides/*.html 的 font-size 与行内 padding（--dry 只报告）；改完请再跑 render_deck.js 自查。
//   幂等：首次运行把规格字号的原稿存到 project 同级的 fit_source/（不发布），之后总从原稿重算；改文字改原稿再重跑。
// 规则（与 skill §4 字号表一致）：
//   不动：h1、≥40px 的大数、图片、底图上的定位标签（E2/E3 节点与读数标签）。
//   固定抬高：等宽标签/页脚 18–20 → 22（窗口标题栏 18 → 20）；页脚与以“来源”开头的说明行 → 22。
//   标题 h2：40→44、44→48、46→50、48→52，超过 2 行或末行孤字则每次退 2px（不低于原值；仍有孤字就改标题措辞）。
//   可伸缩正文：20–22 → 26、23–24 → 28、27 → 34，上限 = 基准 + 4；整页同一步进 k 一起放大。
//   约束：不越界、不横向溢出、正文不触页脚（页脚 top − 8）、绝对定位容器不溢出、标题 ≤ 2 行；
//         在不低于基准的可行步进里优先选“无孤字”（末行 < 3 个字宽，含单独掉行的引用编号）的最大值。
//   剩余空间：字号到顶后，带 border-top 且 padding 为 “Npx 0” 的列表行把剩余高度平分到上下 padding（每行 ≤ +24px）。
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const [DECK, MAP, FLAG] = process.argv.slice(2); const DRY = FLAG === '--dry';
const blobs = MAP.endsWith('.json') ? JSON.parse(fs.readFileSync(MAP)) :
  Object.fromEntries(fs.readFileSync(MAP, 'utf8').split('\n').filter(l => l.trim()).map(l => { const [k, v] = l.trim().split(/\s+/); return [k, path.resolve(v)]; }));
const order = JSON.parse(fs.readFileSync(`${DECK}/deck.json`)).order;
const SRC = path.join(path.dirname(path.resolve(DECK)), 'fit_source'); fs.mkdirSync(SRC, { recursive: true });
const CSS = `<style>html,body{margin:0;background:#888}section{position:relative;width:1920px;height:1080px;overflow:hidden;box-sizing:border-box}
section *{box-sizing:border-box;margin:0}ul,ol{padding-left:1.2em}table{border-collapse:collapse}td,th{border:1px solid #c9c8c2;padding:.35em .6em;vertical-align:top;text-align:left}
aside{display:none}img{display:block}div:not([style*="display"]){display:flex;flex-direction:column}div[style*="display:flex"]:not([style*="flex-direction"]){flex-direction:row}</style>`;
const TAG = /<(p|h1|h2|h3|li|div)\b([^>]*)>/g;

function tagIndex(src) { let i = 0; return src.replace(TAG, (m, t, rest) => `<${t} data-fit-i="${i++}"${rest}>`); }
function toBrowser(src) {
  return src.replace(/\/_blob\/([0-9a-f]{32})/g, (m, id) => 'file://' + (blobs[id] || '/nonexistent'))
    .replaceAll("'Noto Sans SC'", "'Noto Sans CJK SC'").replaceAll("'Noto Serif SC'", "'Noto Serif CJK SC'")
    .replaceAll("'JetBrains Mono'", "'DejaVu Sans Mono'").replaceAll("'IBM Plex Mono'", "'DejaVu Sans Mono'");
}

// ---- runs in the page ----
const PAGE = () => {
  const sec = document.querySelector('section'); const $ = s => [...sec.querySelectorAll(s)];
  const px = el => parseFloat(el.style.fontSize || getComputedStyle(el).fontSize);
  const isMono = el => /Mono/.test(el.style.fontFamily || '');
  const pinned = el => { for (let e = el; e && e !== sec; e = e.parentElement) if (e.style.position === 'absolute') return e; return null; };
  const roles = {}; const orig = {};
  for (const el of $('[data-fit-i]')) {
    if (el.tagName === 'DIV' || el.tagName === 'H1') continue;
    const f = px(el); const i = el.dataset.fitI; orig[i] = f; const pin = pinned(el);
    const pinnedSelf = el.style.position === 'absolute';
    const isFooter = pinnedSelf && el.style.bottom;
    if (el.tagName === 'H2') { roles[i] = { kind: 'title', base: { 40: 44, 44: 48, 46: 50, 48: 52 }[f] || f, min: f }; continue; }
    if (f >= 40) continue;
    if (isFooter || /^来源/.test(el.textContent.trim())) { roles[i] = { kind: 'fixed', size: 22 }; continue; }
    if (pinnedSelf) continue;                       // node / readout labels on backgrounds
    if (isMono(el)) { roles[i] = { kind: 'fixed', size: f <= 18 ? 20 : 22 }; continue; }
    const base = f <= 22 ? 26 : f <= 24 ? 28 : f <= 27 ? 34 : f + 2;
    roles[i] = { kind: 'body', base, cap: base + 4, min: f, inPin: !!pin };
  }
  const rows = $('div[data-fit-i]').filter(d => /border-top/.test(d.getAttribute('style')) && /padding:(\d+)px 0(;|")/.test(d.getAttribute('style') + '"') && !pinned(d));
  const rowPad = Object.fromEntries(rows.map(d => [d.dataset.fitI, parseInt(d.getAttribute('style').match(/padding:(\d+)px 0/)[1])]));
  function apply(k, tShift, extra) {
    for (const [i, r] of Object.entries(roles)) {
      const el = sec.querySelector(`[data-fit-i="${i}"]`);
      if (r.kind === 'fixed') el.style.fontSize = r.size + 'px';
      if (r.kind === 'title') el.style.fontSize = Math.max(r.min, r.base - tShift) + 'px';
      if (r.kind === 'body') el.style.fontSize = Math.max(r.min, Math.min(r.cap, r.base + 2 * k)) + 'px';
    }
    for (const [i, p] of Object.entries(rowPad)) sec.querySelector(`[data-fit-i="${i}"]`).style.padding = `${p + extra}px 0`;
  }
  function measure() {
    const kids = [...sec.children];
    let footTop = 1080; for (const p of kids) { const b = p.getBoundingClientRect(); if (getComputedStyle(p).position === 'absolute' && b.top > 900 && b.height < 120) footTop = Math.min(footTop, b.top); }
    const flow = kids.filter(e => getComputedStyle(e).position !== 'absolute' && e.tagName !== 'ASIDE');
    const padTop = parseFloat(getComputedStyle(sec).paddingTop);
    let flowBottom = 0; for (const f of flow) flowBottom = Math.max(flowBottom, f.getBoundingClientRect().bottom);
    const bad = [];
    for (const e of sec.querySelectorAll('*')) { if (e.tagName === 'ASIDE' || e.tagName === 'IMG') continue; const b = e.getBoundingClientRect();
      if (b.width && (b.right > 1921 || b.bottom > 1081)) bad.push('edge'); if (/^(P|H2|H3)$/.test(e.tagName) && e.scrollWidth > e.clientWidth + 2) bad.push('hscroll'); }
    const fullBleed = !padTop && flow.length === 0;
    if (!fullBleed && flow.length && flowBottom > footTop - 8 && sec.style.padding !== '0px') bad.push('foot');
    for (const c of kids) { if (c.tagName !== 'DIV' || getComputedStyle(c).position !== 'absolute') continue;
      const cb = c.getBoundingClientRect(); if (cb.height < 300) continue;
      let lb = 0; for (const d of c.querySelectorAll('p,h1,h2,h3,img')) lb = Math.max(lb, d.getBoundingClientRect().bottom);
      if (lb > cb.bottom + 1) bad.push('box'); }
    if (sec.style.padding === '0px' || sec.style.padding === '0') for (const d of sec.children) { if (d.tagName !== 'DIV') continue; const db = d.getBoundingClientRect();
      for (const c of d.querySelectorAll('p,h1,h2,h3,img')) if (c.getBoundingClientRect().bottom > db.bottom + 1) { bad.push('box'); break; } }
    let titleLines = 0; for (const h of sec.querySelectorAll('h2')) titleLines = Math.max(titleLines, Math.round(h.getBoundingClientRect().height / parseFloat(getComputedStyle(h).lineHeight)));
    let orphans = 0; const orphanText = [];
    for (const [i, r] of Object.entries(roles)) { if (r.kind !== 'body') continue; const el = sec.querySelector(`[data-fit-i="${i}"]`);
      const rg = document.createRange(); rg.selectNodeContents(el); const rects = [...rg.getClientRects()]; const lines = {};
      for (const q of rects) { const t = Math.round(q.top / 4); lines[t] = (lines[t] || 0) + q.width; }
      const ws = Object.entries(lines).sort((a, b) => a[0] - b[0]).map(x => x[1]);
      if (ws.length > 1 && ws[ws.length - 1] < 3 * parseFloat(el.style.fontSize)) { orphans++; orphanText.push(el.textContent.slice(0, 18)); } }
    const limit = footTop - 8; const fill = flow.length && padTop ? (flowBottom - padTop) / (limit - padTop) : null;
    return { bad: [...new Set(bad)], titleLines, orphans, fill, residual: flow.length && padTop ? limit - flowBottom : 0, orphanText };
  }
  // title shift first (≤2 lines at base body)
  let t = 0; apply(0, 0, 0);
  const titleOrphan = () => [...sec.querySelectorAll('h2')].some(h => { const rg = document.createRange(); rg.selectNodeContents(h);
    const L = {}; for (const q of rg.getClientRects()) { const k = Math.round(q.top / 4); L[k] = (L[k] || 0) + q.width; }
    const ws = Object.entries(L).sort((a, b) => a[0] - b[0]).map(x => x[1]); return ws.length > 1 && ws[ws.length - 1] < 3 * parseFloat(getComputedStyle(h).fontSize); });
  while ((measure().titleLines > 2 || titleOrphan()) && t < 12) { t += 2; apply(0, t, 0); }
  // body step: from -3 (toward original) to +2 (cap = base+4)
  const ok = []; for (let k = -3; k <= 2; k++) { apply(k, t, 0); const m = measure(); if (!m.bad.length && m.titleLines <= 2) ok.push({ k, m }); }
  // 不为躲孤字而退到基准以下：基准及以上优先无孤字，否则取最大可行值并报告孤字行，由人删改文字
  const atBase = ok.filter(o => o.k >= 0);
  let pick = atBase.filter(o => o.m.orphans === 0).pop() || atBase.pop() || ok.filter(o => o.m.orphans === 0).pop() || ok.pop() || { k: -3, m: null };
  apply(pick.k, t, 0); let m = measure(); let extra = 0;
  if (Object.keys(rowPad).length && m.residual > 40) {
    extra = Math.min(24, Math.floor(m.residual / (2 * Object.keys(rowPad).length)));
    while (extra > 0) { apply(pick.k, t, extra); const mm = measure(); if (!mm.bad.length) { m = mm; break; } extra -= 2; }
    if (extra <= 0) { extra = 0; apply(pick.k, t, 0); m = measure(); }
  }
  const out = {}; for (const [i, r] of Object.entries(roles)) { const el = sec.querySelector(`[data-fit-i="${i}"]`); if (el.style.fontSize !== orig[i] + 'px') out[i] = el.style.fontSize; }
  const pads = {}; if (extra) for (const [i, p] of Object.entries(rowPad)) pads[i] = `${p + extra}px 0`;
  return { out, pads, k: pick.k, tShift: t, extra, fill: m.fill && +m.fill.toFixed(2), orphans: m.orphans, orphanText: m.orphanText, bad: m.bad, noFit: !ok.length };
};

(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } }); const tmp = path.join(require('os').tmpdir(), 'fit_text_tmp.html');
  for (const sid of order) {
    const file = `${DECK}/slides/${sid}.html`; const keep = path.join(SRC, `${sid}.html`);
    // 幂等：第一次运行把规格字号的源文件存进 fit_source/，之后一律从源文件重算；改文字请改 fit_source/ 里的文件
    if (!fs.existsSync(keep)) fs.copyFileSync(file, keep);
    const src = fs.readFileSync(keep, 'utf8');
    fs.writeFileSync(tmp, `<!doctype html><html><head><meta charset=utf-8>${CSS}</head><body>${toBrowser(tagIndex(src))}</body></html>`);
    await pg.goto('file://' + tmp); await pg.waitForTimeout(80);
    const r = await pg.evaluate(PAGE);
    let i = 0; const next = src.replace(TAG, (m, t) => {
      const id = String(i++); let tag = m;
      if (r.out[id]) tag = /font-size:\s*[\d.]+px/.test(tag) ? tag.replace(/font-size:\s*[\d.]+px/, 'font-size:' + r.out[id]) : tag.replace(/style="/, `style="font-size:${r.out[id]};`);
      if (r.pads[id]) tag = tag.replace(/padding:\d+px 0(?=[;"])/, 'padding:' + r.pads[id]);
      return tag; });
    if (!DRY && next !== src) fs.writeFileSync(file, next);
    const flag = r.noFit ? ' NO-FIT' : (r.fill !== null && r.fill < 0.6 ? ' LOW-FILL' : '');
    console.log(sid.padEnd(16), `k=${r.k} title-${r.tShift} pad+${r.extra} fill=${r.fill ?? '-'} orphans=${r.orphans} ${r.bad.join(',')}${flag}${r.orphanText.length ? '  孤字：' + r.orphanText.join(' | ') : ''}`);
  }
  await b.close();
})();
