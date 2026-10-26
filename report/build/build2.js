// Report builder v2: per-chapter sections, exhibit titles above, key-point boxes, stat tiles, gap callouts
const fs = require("fs");
const path = require("path");
const {
  LineRuleType, Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, ImageRun, PageBreak, Footer, Header, PageNumber, TabStopType,
  LevelFormat, VerticalAlign, SectionType, TableLayoutType, PageOrientation, VerticalMergeType,
} = require("docx");

const ROOT = "/home/claude/report";
const CONTENT = path.join(ROOT, "content");
const FILES = ["00_front.md", "01_ch1.md", "02_ch2.md", "03_ch3.md", "04_ch4.md", "05_ch5.md", "06_ch6.md", "07_ch7.md", "08_ch8.md", "refs.md", "09_appendix.md"];
const tocPages = fs.existsSync(path.join(ROOT, "build/toc_pages.json")) ? JSON.parse(fs.readFileSync(path.join(ROOT, "build/toc_pages.json"), "utf8")) : {};
const SHORT_TITLE = "AI 编程工具行业分析报告（2026）";

// ---------- palette & metrics ----------
const FONT_CJK = "Microsoft YaHei", FONT_LATIN = "Calibri";
const NAVY = "14365F";      // headings, table heads
const ACCENT = "2A78D6";    // single accent
const INK = "222222", GREY = "5F5E5A", MUTED = "8A8984", RULE = "C9C8C2";
const TINT = "EEF4FB";      // accent tint
const AMBER = "B26A00", AMBER_TINT = "FFF6E5";
const BODY = 20;            // 10pt
const PAGE_W = 11906, PAGE_H = 16838;
const ML = 1247, MR = 1247, MT = 1361, MB = 1304;   // ~2.2cm sides
const TEXT_W = PAGE_W - ML - MR;
const LAND_W = PAGE_H - ML - MR;
const curW = () => (cur && cur.opts.land ? LAND_W : TEXT_W);
const fonts = { ascii: FONT_LATIN, hAnsi: FONT_LATIN, eastAsia: FONT_CJK, cs: FONT_LATIN };
const CN = { "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10 };

// ---------- pass 1: exhibit numbering ----------
const LABELS = {};
const EXH = [];
(function numberExhibits() {
  let chap = null, fi = 0, ti = 0;
  for (const f of FILES) {
    for (const L of fs.readFileSync(path.join(CONTENT, f), "utf8").split("\n")) {
      let m;
      if ((m = L.match(/^# 第(.)章/))) { chap = String(CN[m[1]]); fi = 0; ti = 0; }
      else if ((m = L.match(/^## 附录 ([A-Z])/))) { chap = m[1]; fi = 0; ti = 0; }
      if ((m = L.match(/^FIG:.*\{#(\w+)\}\s*([^|]+)/))) { LABELS[m[1]] = `图 ${chap}-${++fi}`; EXH.push({ label: LABELS[m[1]], title: m[2].trim() }); }
      if ((m = L.match(/^TABLE:\s*\{#(\w+)[^}]*\}\s*(.*)$/))) { LABELS[m[1]] = `表 ${chap}-${++ti}`; EXH.push({ label: LABELS[m[1]], title: m[2].trim() }); }
    }
  }
})();
function resolveRefs(t) {
  return t.replace(/\[\[(图|表):(\w+)\]\]/g, (_, k, key) => {
    if (!LABELS[key]) throw new Error("unknown label " + key);
    return LABELS[key];
  });
}

// ---------- inline runs ----------
function runs(text, o = {}) {
  text = resolveRefs(text);
  const size = o.size || BODY;
  const out = [];
  const toks = text.split(/(\*\*[^*]+\*\*|〔证据：[^〕]+〕|\[\d+\](?:\[\d+\])*(?:–\[\d+\])?)/g);
  for (const p of toks) {
    if (!p) continue;
    if (p.startsWith("**")) out.push(new TextRun({ text: p.slice(2, -2), bold: true, font: fonts, size, color: o.boldColor || o.color || INK }));
    else if (p.startsWith("〔证据")) {
      const lvl = p.slice(4, -1);
      const col = lvl.startsWith("强") ? NAVY : lvl.startsWith("弱") ? MUTED : AMBER;
      out.push(new TextRun({ text: " 证据" + "·" + lvl, font: fonts, size: size - 3, bold: true, color: col }));
    } else if (/^\[\d+\]/.test(p)) out.push(new TextRun({ text: p, font: fonts, size: size - 4, color: "4A72A8" }));
    else out.push(new TextRun({ text: p, font: fonts, size, color: o.color || INK, italics: o.italics }));
  }
  return out;
}
const P = (children, o = {}) => new Paragraph({ children, alignment: o.align ?? AlignmentType.JUSTIFIED, spacing: { before: o.before ?? 0, after: o.after ?? 120, line: o.line ?? 320, lineRule: LineRuleType.AUTO }, indent: o.indent, keepNext: o.keepNext, keepLines: o.keepLines, shading: o.shading, border: o.border, pageBreakBefore: o.pageBreakBefore });
const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: none, bottom: none, left: none, right: none, insideHorizontal: none, insideVertical: none };

// ---------- blocks ----------
function exhibitTitle(label, title, sub, keep = true) {
  const out = [P([new TextRun({ text: label + "  ", font: fonts, size: 19, bold: true, color: ACCENT }), new TextRun({ text: title, font: fonts, size: 19, bold: true, color: NAVY })],
    { align: AlignmentType.LEFT, before: 200, after: sub ? 20 : 80, line: 290, keepNext: keep, keepLines: true })];
  if (sub) out.push(P([new TextRun({ text: sub, font: fonts, size: 16, color: GREY })], { align: AlignmentType.LEFT, after: 80, line: 260, keepNext: keep, keepLines: true }));
  return out;
}
function sourceNote(text) {
  return P(runs(text, { size: 15, color: MUTED }), { align: AlignmentType.LEFT, before: 40, after: 220, line: 250, border: { top: { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 3 } } });
}
function figure(file, label, title, sub, src) {
  const buf = fs.readFileSync(path.join(ROOT, file));
  const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);
  const maxW = (TEXT_W / 1440) * 96 * 0.97;
  let dw = maxW, dh = Math.round(h * maxW / w);
  const maxH = 5.6 * 96;
  if (dh > maxH) { dh = maxH; dw = Math.round(w * maxH / h); }
  return [
    ...exhibitTitle(label, title, sub),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 20, line: 240, lineRule: LineRuleType.AUTO }, keepNext: true, children: [new ImageRun({ type: "png", data: buf, transformation: { width: Math.round(dw), height: Math.round(dh) } })] }),
    sourceNote(src),
  ];
}
function cell(children, w, o = {}) {
  return new TableCell({ width: { size: w, type: WidthType.DXA }, children, verticalAlign: o.valign ?? VerticalAlign.CENTER,
    shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: "auto" } : undefined,
    margins: { top: o.mt ?? 60, bottom: o.mb ?? 60, left: o.ml ?? 90, right: o.mr ?? 90 }, borders: o.borders, columnSpan: o.span, verticalMerge: o.vmerge });
}
function brk(t) { return t.replace(/([、；，：（）＋+])(?=[A-Za-z0-9./(])/g, "$1\u200B").replace(/(?<=[A-Za-z0-9.)])([、；，（])/g, "\u200B$1").replace(/(?<=[A-Za-z0-9)）])\/(?=[A-Za-z0-9.(（])/g, "/\u200B").replace(/(?<=[a-z])\.(?=[A-Za-z]{2,})/g, "\u200B."); }
function dataTable(header, rows, widths, o = {}) {
  const fsz = o.fs || 16, mx = o.fs && o.fs < 16 ? 70 : 90;
  const hb = { style: BorderStyle.SINGLE, size: 4, color: RULE };
  const rowB = { top: none, left: none, right: none, bottom: hb };
  const head = new TableRow({ tableHeader: true, children: header.map((h, i) => cell([P([new TextRun({ text: brk(h), bold: true, color: "FFFFFF", font: fonts, size: fsz })], { align: AlignmentType.LEFT, after: 0, line: 250 })], widths[i], { fill: NAVY, ml: mx, mr: mx, borders: { top: none, left: none, right: none, bottom: none } })) });
  const vm = (ri, i) => rows[ri][i] === "^" ? VerticalMergeType.CONTINUE : (rows[ri + 1] && rows[ri + 1][i] === "^" ? VerticalMergeType.RESTART : undefined);
  const body = rows.map((r, ri) => new TableRow({ cantSplit: !o.split, children: r.map((c, i) => cell([P(runs(brk(c === "^" ? "" : c), { size: fsz }), { align: AlignmentType.LEFT, after: 0, line: 250, keepNext: o.keep || (o.tail && ri === rows.length - 2) })], widths[i], { fill: ri % 2 ? "F6F8FB" : undefined, ml: mx, mr: mx, borders: rowB, vmerge: vm(ri, i) })) }));
  return new Table({ width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths, layout: TableLayoutType.FIXED, borders: noBorders, rows: [head, ...body] });
}
function defaultWidths(n) {
  const preset = { 2: [28, 72], 3: [18, 52, 30], 4: [18, 30, 22, 30], 5: [16, 20, 18, 22, 24], 6: [17, 17, 15, 13, 22, 16], 7: [16, 12, 12, 16, 16, 14, 14], 10: [10, 9, 10, 11, 12, 10, 10, 9, 10, 9] };
  return preset[n] || Array(n).fill(100 / n);
}
function pctToDxa(p) {
  const tot = p.reduce((a, b) => a + b, 0);
  const W = curW();
  const ws = p.map(x => Math.floor(W * x / tot));
  ws[ws.length - 1] += W - ws.reduce((a, b) => a + b, 0);
  return ws;
}
function defCard(text) {
  const b = { style: BorderStyle.SINGLE, size: 24, color: ACCENT };
  return [new Table({ width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: [TEXT_W], borders: noBorders, rows: [new TableRow({ children: [
    cell([P(runs(text, { size: 21, boldColor: NAVY }), { align: AlignmentType.LEFT, after: 0, line: 330 })], TEXT_W, { fill: TINT, borders: { left: b, top: none, bottom: none, right: none }, mt: 120, mb: 120, ml: 200, mr: 200 }),
  ] })] }), P([], { after: 120 })];
}
function gapBox(text) {
  const b = { style: BorderStyle.SINGLE, size: 24, color: "E0A030" };
  return [new Table({ width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: [TEXT_W], borders: noBorders, rows: [new TableRow({ cantSplit: true, children: [
    cell([P([new TextRun({ text: "证据缺口 · 待核实  ", bold: true, font: fonts, size: 17, color: AMBER }), ...runs(text, { size: 17, color: "4A4A46" })], { align: AlignmentType.JUSTIFIED, after: 0, line: 290 })], TEXT_W, { fill: AMBER_TINT, borders: { left: b, top: none, bottom: none, right: none }, mt: 90, mb: 90, ml: 180, mr: 180 }),
  ] })] }), P([], { after: 100 })];
}
function keyPoints(rows) {
  const lw = 1050, rw = TEXT_W - lw;
  const fills = { "事实": "8A8984", "机制": "5F93DD", "判断": NAVY };
  const thin = { style: BorderStyle.SINGLE, size: 4, color: "FFFFFF" };
  const title = new TableRow({ children: [cell([P([new TextRun({ text: "本章要点", bold: true, font: fonts, size: 18, color: NAVY })], { align: AlignmentType.LEFT, after: 0, line: 260 })], TEXT_W, { span: 2, fill: TINT, borders: { top: none, left: none, right: none, bottom: thin }, mt: 70, mb: 50, ml: 140 })] });
  const trs = rows.map(([k, v]) => new TableRow({ cantSplit: true, children: [
    cell([P([new TextRun({ text: k, bold: true, font: fonts, size: 18, color: "FFFFFF" })], { align: AlignmentType.CENTER, after: 0, line: 260 })], lw, { fill: fills[k] || NAVY, borders: { top: thin, bottom: thin, left: none, right: none } }),
    cell([P(runs(v, { size: 18 }), { align: AlignmentType.JUSTIFIED, after: 0, line: 290 })], rw, { fill: TINT, borders: { top: thin, bottom: thin, left: none, right: none }, ml: 160, mr: 160 }),
  ] }));
  return [new Table({ width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: [lw, rw], borders: noBorders, rows: [title, ...trs] }), P([], { after: 160 })];
}
function statTiles(title, items) {
  const cols = 4, gw = Math.floor(TEXT_W / cols);
  const widths = Array(cols).fill(gw); widths[cols - 1] += TEXT_W - gw * cols;
  const white = { style: BorderStyle.SINGLE, size: 24, color: "FFFFFF" };
  const rows = [];
  for (let r = 0; r < items.length; r += cols) {
    rows.push(new TableRow({ cantSplit: true, children: items.slice(r, r + cols).map((it, j) => {
      const [num, label, tag] = it;
      return cell([
        P([new TextRun({ text: num, bold: true, font: fonts, size: 34, color: NAVY })], { align: AlignmentType.LEFT, after: 30, line: 360 }),
        P(runs(label, { size: 15, color: "3D3D3A" }), { align: AlignmentType.LEFT, after: 30, line: 240 }),
        P([new TextRun({ text: tag, font: fonts, size: 13, color: ACCENT, bold: true })], { align: AlignmentType.LEFT, after: 0, line: 220 }),
      ], widths[j], { fill: "F3F6FA", valign: VerticalAlign.TOP, borders: { top: { style: BorderStyle.SINGLE, size: 18, color: ACCENT }, bottom: white, left: white, right: white }, mt: 110, mb: 110, ml: 130, mr: 110 });
    }) }));
  }
  return [P([new TextRun({ text: title, bold: true, font: fonts, size: 20, color: NAVY })], { align: AlignmentType.LEFT, before: 120, after: 80, keepNext: true }),
    new Table({ width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: widths, borders: noBorders, rows }), P([], { after: 160 })];
}
function caseBox(lines) {
  const b = { style: BorderStyle.SINGLE, size: 6, color: "9FBFE6" };
  const children = [
    P([new TextRun({ text: "案例  ", bold: true, font: fonts, size: 18, color: "FFFFFF", shading: { type: ShadingType.CLEAR, fill: ACCENT, color: "auto" } }), new TextRun({ text: "  " + lines[0].replace(/^案例 \d+ /, ""), bold: true, font: fonts, size: 20, color: NAVY })], { align: AlignmentType.LEFT, after: 100, line: 300, keepNext: true }),
    ...lines.slice(1).map(l => P(runs(l, { size: 18, boldColor: NAVY }), { after: 70, line: 300 })),
  ];
  const caseNo = (lines[0].match(/^案例 (\d+)/) || [])[1];
  if (caseNo) children[0] = P([new TextRun({ text: ` 案例 ${caseNo} `, bold: true, font: fonts, size: 17, color: "FFFFFF", shading: { type: ShadingType.CLEAR, fill: ACCENT, color: "auto" } }), new TextRun({ text: "  " + lines[0].replace(/^案例 \d+ /, ""), bold: true, font: fonts, size: 20, color: NAVY })], { align: AlignmentType.LEFT, after: 100, line: 300, keepNext: true });
  const nC = children.length;
  const rowsC = children.map((p, k) => new TableRow({ cantSplit: true, children: [cell([p], TEXT_W, { fill: "F7FAFE", borders: { top: k === 0 ? b : none, bottom: k === nC - 1 ? b : none, left: b, right: b }, mt: k === 0 ? 140 : 0, mb: k === nC - 1 ? 120 : 0, ml: 220, mr: 220 })] }));
  return [new Table({ width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: [TEXT_W], borders: noBorders, rows: rowsC }), P([], { after: 140 })];
}

// ---------- sections ----------
const sections = [];
let cur = null;
function newSection(name, opts = {}) { cur = { name, children: [], opts }; sections.push(cur); }
const push = (...xs) => cur.children.push(...xs);

function cover(title, sub, meta) {
  const band = new Table({ width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: [TEXT_W], borders: noBorders, rows: [new TableRow({ height: { value: 90, rule: "exact" }, children: [cell([P([], { after: 0 })], TEXT_W, { fill: ACCENT, borders: { top: none, bottom: none, left: none, right: none }, mt: 0, mb: 0 })] })] });
  push(P([], { before: 1700, after: 0 }), band,
    P([new TextRun({ text: "行业分析报告 · 2026", font: fonts, size: 22, color: ACCENT, bold: true })], { align: AlignmentType.LEFT, before: 240, after: 360 }),
    P([new TextRun({ text: title, font: fonts, size: 50, bold: true, color: NAVY })], { align: AlignmentType.LEFT, after: 240, line: 560 }),
    P([new TextRun({ text: sub, font: fonts, size: 24, color: GREY })], { align: AlignmentType.LEFT, after: 1300 }),
    P([new TextRun({ text: "研究重点", font: fonts, size: 18, bold: true, color: NAVY })], { align: AlignmentType.LEFT, after: 60 }),
    P([new TextRun({ text: "编程基础较弱、主要依靠自然语言开发的个人与小型研发团队，在维护已有网站、Web 应用和线上业务工具时的需求与困难", font: fonts, size: 19, color: GREY })], { align: AlignmentType.LEFT, after: 2600, line: 320 }),
    ...meta.map(m => P([new TextRun({ text: m, font: fonts, size: 16, color: MUTED })], { align: AlignmentType.LEFT, after: 60 })),
    P([new TextRun({ text: "2026 年 10 月", font: fonts, size: 20, color: NAVY, bold: true })], { align: AlignmentType.LEFT, before: 200 }),
  );
}
function tocBlock() {
  push(P([new TextRun({ text: "目录", font: fonts, size: 34, bold: true, color: NAVY })], { align: AlignmentType.LEFT, after: 300, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: ACCENT, space: 6 } } }));
  push(P([new TextRun({ text: "TOCSTART", size: 2, color: "FFFFFF" })], { after: 0 }));
  for (const e of (tocPages.entries || [])) {
    const l1 = e.level === 1;
    push(new Paragraph({ spacing: { after: l1 ? 50 : 10, before: l1 ? 150 : 0, line: 270 }, indent: { left: l1 ? 0 : 420 },
      tabStops: [{ type: TabStopType.RIGHT, position: TEXT_W, leader: "dot" }],
      children: [new TextRun({ text: e.text, font: fonts, size: l1 ? 20 : 18, bold: l1, color: l1 ? NAVY : INK }), new TextRun({ text: "\t" + e.page, font: fonts, size: l1 ? 20 : 18, bold: l1, color: l1 ? NAVY : INK })] }));
  }
  push(P([new TextRun({ text: "TOCEND", size: 2, color: "FFFFFF" })], { after: 0 }));
  newSection("图表目录", { cols2: true });
  push(P([new TextRun({ text: "图表目录", font: fonts, size: 28, bold: true, color: NAVY })], { align: AlignmentType.LEFT, after: 200, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: ACCENT, space: 6 } } }));
  const pages = fs.existsSync(path.join(ROOT, "build/exhibit_pages.json")) ? JSON.parse(fs.readFileSync(path.join(ROOT, "build/exhibit_pages.json"), "utf8")) : {};
  const colW = Math.floor((TEXT_W - 420) / 2);
  for (const kind of ["图", "表"]) {
    push(P([new TextRun({ text: kind === "图" ? "图" : "表", font: fonts, size: 18, bold: true, color: ACCENT })], { align: AlignmentType.LEFT, before: kind === "表" ? 160 : 0, after: 60, keepNext: true }));
    for (const e of EXH.filter(x => x.label.startsWith(kind))) {
      push(new Paragraph({ spacing: { after: 30, line: 230, lineRule: LineRuleType.AUTO }, indent: { left: 640, hanging: 640, right: 300 },
        tabStops: [{ type: TabStopType.LEFT, position: 640 }, { type: TabStopType.RIGHT, position: colW, leader: "dot" }],
        children: [new TextRun({ text: e.label.replace(/^[图表] /, ""), font: fonts, size: 14, bold: true, color: NAVY }), new TextRun({ text: "\t" + e.title, font: fonts, size: 14, color: INK }), new TextRun({ text: "\t" + (pages[e.label] || "00"), font: fonts, size: 14, color: GREY })] }));
    }
  }
  fs.writeFileSync(path.join(ROOT, "build/exhibits.json"), JSON.stringify(EXH, null, 0));
}

function parseFile(fname) {
  const lines = fs.readFileSync(path.join(CONTENT, fname), "utf8").split("\n");
  let i = 0;
  while (i < lines.length) {
    const L = lines[i];
    if (L.trim() === "") { i++; continue; }
    if (L.startsWith("COVER")) {
      const meta = []; let title = "", sub = ""; i++;
      while (!lines[i].startsWith("ENDCOVER")) {
        if (lines[i].startsWith("TITLE:")) title = lines[i].slice(6).trim();
        else if (lines[i].startsWith("SUBTITLE:")) sub = lines[i].slice(9).trim();
        else if (lines[i].startsWith("META:")) meta.push(lines[i].slice(5).trim());
        i++;
      }
      i++; newSection("cover", { cover: true }); cover(title, sub, meta); continue;
    }
    if (L.startsWith("PAGEBREAK")) { i++; continue; }
    if (L.trim() === "LANDSCAPE") { newSection(cur.name, { ...cur.opts, land: true }); i++; continue; }
    if (L.trim() === "PORTRAIT") { newSection(cur.name, { ...cur.opts, land: false }); i++; continue; }  // sections handle breaks
    if (L.startsWith("TOC")) { newSection("目录"); tocBlock(); i++; continue; }
    if (L.startsWith("# ")) {
      const t = L.slice(2).trim();
      newSection(t, { refs: fname === "refs.md" });
      push(new Paragraph({ text: t, heading: HeadingLevel.HEADING_1, keepNext: true }));
      i++; continue;
    }
    if (L.startsWith("## ")) { push(new Paragraph({ text: L.slice(3).trim(), heading: HeadingLevel.HEADING_2, keepNext: true })); i++; continue; }
    if (L.startsWith("### ")) { push(new Paragraph({ text: L.slice(4).trim(), heading: HeadingLevel.HEADING_3, keepNext: true })); i++; continue; }
    if (L.startsWith("DEF:")) { push(...defCard(L.slice(4).trim())); i++; continue; }
    if (L.startsWith("GAP:")) { push(...gapBox(L.slice(4).trim())); i++; continue; }
    if (L.startsWith("KEYPOINTS")) {
      i++; const rows = [];
      while (!lines[i].startsWith("ENDKEY")) { const [k, ...v] = lines[i].split("|"); rows.push([k.trim(), v.join("|").trim()]); i++; }
      i++; push(...keyPoints(rows)); continue;
    }
    if (L.startsWith("STATS:")) {
      const t = L.slice(6).trim(); i++; const items = [];
      while (!lines[i].startsWith("ENDSTATS")) { items.push(lines[i].split("|").map(s => s.trim())); i++; }
      i++; push(...statTiles(t, items)); continue;
    }
    if (L.startsWith("FIG:")) {
      const parts = L.slice(4).split("|").map(s => s.trim());
      const key = parts[1].match(/\{#(\w+)\}/)[1];
      const title = parts[1].replace(/\{#\w+\}\s*/, "");
      push(...figure(parts[0], LABELS[key], title, parts.length === 4 ? parts[2] : null, parts[parts.length - 1]));
      i++; continue;
    }
    if (L.startsWith("TABLE:")) {
      const m = L.match(/^TABLE:\s*\{#(\w+)([^}]*)\}\s*(.*)$/);
      const key = m[1], optstr = m[2], title = m[3]; i++;
      const wspec = (optstr.match(/w=([\d.,]+)/) || [])[1];
      const topt = { fs: +((optstr.match(/fs=(\d+)/) || [])[1] || 0) || undefined, split: /\bsplit\b/.test(optstr), keep: /\bkeep\b/.test(optstr), tail: /\btail\b/.test(optstr) };
      const tl = [];
      while (i < lines.length && lines[i].startsWith("|")) { tl.push(lines[i]); i++; }
      let src = "";
      if (i < lines.length && lines[i].startsWith("SOURCE:")) { src = lines[i].slice(7).trim(); i++; }
      const rows = tl.filter(l => !/^\|\s*-+/.test(l)).map(l => l.slice(1, -1).split("|").map(c => c.trim()));
      const widths = pctToDxa(wspec ? wspec.split(",").map(Number) : defaultWidths(rows[0].length));
      push(...exhibitTitle(LABELS[key], title, null), dataTable(rows[0], rows.slice(1), widths, topt), sourceNote(src || " "));
      continue;
    }
    if (L.startsWith("> ")) {
      const q = []; while (i < lines.length && lines[i].startsWith("> ")) { q.push(lines[i].slice(2).trim()); i++; }
      push(...caseBox(q)); continue;
    }
    if (/^\d+\.\s/.test(L)) {
      const ref = fname === "00_front.md" ? "findings" : "nums";
      while (i < lines.length && /^\d+\.\s/.test(lines[i])) {
        push(new Paragraph({ numbering: { reference: ref, level: 0 }, alignment: AlignmentType.JUSTIFIED, spacing: { after: ref === "findings" ? 130 : 80, line: 330 }, children: runs(lines[i].replace(/^\d+\.\s/, ""), { boldColor: NAVY }) }));
        i++;
      }
      continue;
    }
    if (L.startsWith("- ")) {
      while (i < lines.length && lines[i].startsWith("- ")) { push(new Paragraph({ numbering: { reference: "bullets", level: 0 }, alignment: AlignmentType.JUSTIFIED, spacing: { after: 80, line: 330 }, children: runs(lines[i].slice(2)) })); i++; }
      continue;
    }
    if (fname === "refs.md" && /^\[\d+\]/.test(L)) {
      push(new Paragraph({ alignment: AlignmentType.LEFT, spacing: { after: 30, line: 230 }, indent: { left: 420, hanging: 420 }, children: runs(L, { size: 14 }) }));
      i++; continue;
    }
    if (fname === "refs.md") { push(P(runs(L, { size: 16, color: GREY }), { after: 100, line: 260 })); i++; continue; }
    push(P(runs(L), { indent: { firstLine: 400 }, after: 100 }));
    i++;
  }
}
for (const f of FILES) parseFile(f);

// ---------- headers / footers ----------
function headerFor(name, w = TEXT_W) {
  return new Header({ children: [new Paragraph({ tabStops: [{ type: TabStopType.RIGHT, position: w }], border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 4 } },
    children: [new TextRun({ text: SHORT_TITLE, font: fonts, size: 14, color: MUTED }), new TextRun({ text: "\t" + name, font: fonts, size: 14, color: NAVY, bold: true })] })] });
}
const footer = new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ children: [PageNumber.CURRENT], font: fonts, size: 16, color: GREY })] })] });
const emptyHF = { header: new Header({ children: [new Paragraph({ children: [] })] }), footer: new Footer({ children: [new Paragraph({ children: [] })] }) };

const pageProps = { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MT, bottom: MB, left: ML, right: MR, header: 680, footer: 620 } };
const docSections = sections.map((s, idx) => ({
  properties: { page: s.opts.land ? { ...pageProps, size: { width: PAGE_W, height: PAGE_H, orientation: PageOrientation.LANDSCAPE } } : pageProps, type: idx === 0 ? undefined : SectionType.NEXT_PAGE, column: (s.opts.refs || s.opts.cols2) ? { count: 2, space: 420 } : undefined },
  headers: s.opts.cover ? { default: emptyHF.header } : { default: headerFor(s.name, s.opts.land ? LAND_W : TEXT_W) },
  footers: s.opts.cover ? { default: emptyHF.footer } : { default: footer },
  children: s.children,
}));

const doc = new Document({
  creator: "行业分析课程研究",
  title: "面向独立开发者与小型研发团队的 AI 编程工具行业分析报告（2026）",
  styles: {
    default: { document: { run: { font: fonts, size: BODY, color: INK }, paragraph: { spacing: { line: 320, lineRule: LineRuleType.AUTO } } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 36, bold: true, color: NAVY, font: fonts }, paragraph: { spacing: { before: 120, after: 320, line: 420 }, outlineLevel: 0, border: { bottom: { style: BorderStyle.SINGLE, size: 18, color: ACCENT, space: 8 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, color: NAVY, font: fonts }, paragraph: { spacing: { before: 360, after: 160, line: 360 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 22, bold: true, color: ACCENT, font: fonts }, paragraph: { spacing: { before: 220, after: 110, line: 330 }, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } }, run: { color: ACCENT } } }] },
    { reference: "nums", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 360 } } } }] },
    { reference: "findings", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 520, hanging: 520 } }, run: { bold: true, color: ACCENT, size: 26 } } }] },
  ] },
  sections: docSections,
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(path.join(ROOT, "build", "report_raw.docx"), buf); console.log("written", buf.length, "sections", docSections.length, "labels", Object.keys(LABELS).length); });
