// Build the DOCX report from markdown-like content files using docx-js
const fs = require("fs");
const path = require("path");
const {
  LineRuleType,
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, ImageRun, PageBreak, Footer, Header, PageNumber, TabStopType,
  LevelFormat, VerticalAlign, PositionalTab, PositionalTabAlignment, PositionalTabLeader, PositionalTabRelativeTo,
} = require("docx");

const ROOT = "/home/claude/report";
const CONTENT = path.join(ROOT, "content");
const FILES = ["00_front.md", "01_ch1.md", "02_ch2.md", "03_ch3.md", "04_ch4.md", "05_ch5.md", "06_ch6.md", "07_ch7.md", "08_ch8.md", "refs.md", "09_appendix.md"];
const tocPages = JSON.parse(fs.existsSync(path.join(ROOT, "build/toc_pages.json")) ? fs.readFileSync(path.join(ROOT, "build/toc_pages.json"), "utf8") : "{}");

// ---------- styling ----------
const FONT_CJK = "Microsoft YaHei";
const FONT_LATIN = "Calibri";
const BLUE = "1F4E79"; const ACCENT = "2A78D6"; const GREY = "595959"; const LIGHT = "F2F2F2"; const HEADFILL = "DCE6F2";
const BODY_SIZE = 21; // 10.5pt
const PAGE_W = 11906, PAGE_H = 16838; // A4 in DXA
const MARGIN = 1440; // 1 inch? use 2.3cm = 1304
const ML = 1304, MR = 1304, MT = 1418, MB = 1418;
const TEXT_W = PAGE_W - ML - MR; // 9298

const fonts = { ascii: FONT_LATIN, hAnsi: FONT_LATIN, eastAsia: FONT_CJK, cs: FONT_LATIN };

function runs(text, opts = {}) {
  // parse **bold** and [n] citations; return TextRun[]
  const out = [];
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  for (const p of parts) {
    if (!p) continue;
    if (p.startsWith("**") && p.endsWith("**")) {
      out.push(new TextRun({ text: p.slice(2, -2), bold: true, font: fonts, size: opts.size || BODY_SIZE, color: opts.color }));
    } else {
      // citations in superscript-ish small grey? keep inline but slightly smaller
      const sub = p.split(/(\[\d+\](?:\[\d+\])*|\[\d+\]–\[\d+\])/g);
      for (const s of sub) {
        if (!s) continue;
        if (/^\[\d+\]/.test(s)) {
          out.push(new TextRun({ text: s, font: fonts, size: (opts.size || BODY_SIZE) - 3, color: "2A5A9B", superScript: false }));
        } else {
          out.push(new TextRun({ text: s, font: fonts, size: opts.size || BODY_SIZE, color: opts.color, italics: opts.italics }));
        }
      }
    }
  }
  return out;
}

function para(text, opts = {}) {
  return new Paragraph({
    children: runs(text, opts),
    alignment: opts.align || AlignmentType.JUSTIFIED,
    spacing: { before: opts.before ?? 0, after: opts.after ?? 120, line: opts.line ?? 340 },
    indent: opts.indent,
    keepNext: opts.keepNext,
    shading: opts.shading,
    border: opts.border,
  });
}

function heading(text, level) {
  const map = { 1: HeadingLevel.HEADING_1, 2: HeadingLevel.HEADING_2, 3: HeadingLevel.HEADING_3 };
  return new Paragraph({ text, heading: map[level], pageBreakBefore: level === 1, keepNext: true });
}

function cellBorders(color = "BFBFBF") {
  const b = { style: BorderStyle.SINGLE, size: 4, color };
  return { top: b, bottom: b, left: b, right: b };
}

function makeTable(headerCells, rows, widths) {
  const total = widths.reduce((a, b) => a + b, 0);
  const mkCell = (txt, w, isHead, shade) => new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: shade ? { type: ShadingType.CLEAR, fill: shade, color: "auto" } : undefined,
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
    verticalAlign: VerticalAlign.CENTER,
    borders: cellBorders(),
    children: [new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: 0, line: 260 },
      children: runs(txt, { size: 17, color: isHead ? "FFFFFF" : undefined }).map(r => r),
    })],
  });
  const headRow = new TableRow({ tableHeader: true, children: headerCells.map((h, i) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: BLUE, color: "auto" },
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
    verticalAlign: VerticalAlign.CENTER,
    borders: cellBorders(),
    children: [new Paragraph({ alignment: AlignmentType.LEFT, spacing: { before: 0, after: 0, line: 260 }, children: [new TextRun({ text: h, bold: true, color: "FFFFFF", font: fonts, size: 17 })] })],
  })) });
  const bodyRows = rows.map((r, ri) => new TableRow({ cantSplit: true, children: r.map((c, i) => mkCell(c, widths[i], false, ri % 2 === 1 ? "F7F9FC" : undefined)) }));
  return new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: widths, rows: [headRow, ...bodyRows] });
}

function colWidths(n, header) {
  // heuristic: distribute by header/content length hints
  const base = Array(n).fill(1);
  if (n === 2) return [Math.round(TEXT_W * 0.28), TEXT_W - Math.round(TEXT_W * 0.28)];
  if (n === 3) return [Math.round(TEXT_W * 0.18), Math.round(TEXT_W * 0.52), TEXT_W - Math.round(TEXT_W * 0.18) - Math.round(TEXT_W * 0.52)];
  if (n === 4) return [0.18, 0.30, 0.22, 0.30].map(f => Math.round(TEXT_W * f));
  if (n === 5) return [0.16, 0.20, 0.18, 0.22, 0.24].map(f => Math.round(TEXT_W * f));
  if (n === 6) return [0.17, 0.17, 0.15, 0.13, 0.22, 0.16].map(f => Math.round(TEXT_W * f));
  if (n === 7) return [0.16, 0.12, 0.12, 0.16, 0.16, 0.14, 0.14].map(f => Math.round(TEXT_W * f));
  if (n === 10) return [0.10, 0.09, 0.10, 0.11, 0.12, 0.10, 0.10, 0.09, 0.10, 0.09].map(f => Math.round(TEXT_W * f));
  const w = Math.floor(TEXT_W / n);
  return Array(n).fill(w);
}

function fixWidths(ws) {
  const total = ws.reduce((a, b) => a + b, 0);
  ws[ws.length - 1] += TEXT_W - total;
  return ws;
}

function caption(text, kind) {
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60, after: 40, line: 280 }, keepNext: kind === "table",
    children: [new TextRun({ text, bold: true, font: fonts, size: 18, color: BLUE })] });
}
function sourceNote(text) {
  return new Paragraph({ alignment: AlignmentType.LEFT, spacing: { before: 20, after: 200, line: 260 },
    children: runs(text, { size: 15, color: GREY }) });
}

function figure(file, cap, src) {
  const abs = path.join(ROOT, file);
  const buf = fs.readFileSync(abs);
  // png size
  const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);
  const targetW = 6.1 * 96; // px at 96dpi for docx-js
  let dw = targetW, dh = Math.round(h * targetW / w);
  const maxH = 7.6 * 96;
  if (dh > maxH) { dh = maxH; dw = Math.round(w * maxH / h); }
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 40 }, keepNext: true,
      children: [new ImageRun({ type: "png", data: buf, transformation: { width: dw, height: dh } })] }),
    caption(cap, "figure"),
    sourceNote(src),
  ];
}

function callout(lines) {
  // boxed case paragraphs
  const children = lines.map((l, i) => new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { before: i === 0 ? 80 : 40, after: i === lines.length - 1 ? 80 : 40, line: 300 },
    indent: { left: 200, right: 200 },
    shading: { type: ShadingType.CLEAR, fill: "F3F7FC", color: "auto" },
    border: i === 0 ? { top: { style: BorderStyle.SINGLE, size: 12, color: ACCENT, space: 4 } } : (i === lines.length - 1 ? { bottom: { style: BorderStyle.SINGLE, size: 12, color: ACCENT, space: 4 } } : undefined),
    children: i === 0 ? [new TextRun({ text: l, bold: true, font: fonts, size: 20, color: BLUE })] : runs(l, { size: 19 }),
  }));
  return children;
}

// ---------- parse ----------
let body = [];
let bulletsConfig = true;

function parseFile(fname) {
  const lines = fs.readFileSync(path.join(CONTENT, fname), "utf8").split("\n");
  let i = 0;
  while (i < lines.length) {
    let L = lines[i];
    if (L.trim() === "") { i++; continue; }
    if (L.startsWith("COVER")) { // cover block
      const meta = []; let title = "", sub = "";
      i++;
      while (!lines[i].startsWith("ENDCOVER")) {
        if (lines[i].startsWith("TITLE:")) title = lines[i].slice(6).trim();
        else if (lines[i].startsWith("SUBTITLE:")) sub = lines[i].slice(9).trim();
        else if (lines[i].startsWith("META:")) meta.push(lines[i].slice(5).trim());
        i++;
      }
      i++;
      body.push(...cover(title, sub, meta));
      continue;
    }
    if (L.startsWith("PAGEBREAK")) { body.push(new Paragraph({ children: [new PageBreak()] })); i++; continue; }
    if (L.startsWith("TOC")) { body.push(...tocBlock()); i++; continue; }
    if (L.startsWith("# ")) { body.push(heading(L.slice(2).trim(), 1)); i++; continue; }
    if (L.startsWith("## ")) { body.push(heading(L.slice(3).trim(), 2)); i++; continue; }
    if (L.startsWith("### ")) { body.push(heading(L.slice(4).trim(), 3)); i++; continue; }
    if (L.startsWith("FIG:")) {
      const [file, cap, src] = L.slice(4).split("|").map(s => s.trim());
      body.push(...figure(file, cap, src)); i++; continue;
    }
    if (L.startsWith("TABLE:")) {
      const cap = L.slice(6).trim(); i++;
      const tlines = [];
      while (i < lines.length && lines[i].startsWith("|")) { tlines.push(lines[i]); i++; }
      let src = "";
      if (i < lines.length && lines[i].startsWith("SOURCE:")) { src = lines[i].slice(7).trim(); i++; }
      const rows = tlines.filter(l => !/^\|\s*-+/.test(l)).map(l => l.slice(1, -1).split("|").map(c => c.trim()));
      const header = rows[0]; const data = rows.slice(1);
      body.push(caption(cap, "table"));
      body.push(makeTable(header, data, fixWidths(colWidths(header.length, header))));
      body.push(sourceNote(src || " "));
      continue;
    }
    if (L.startsWith("> ")) {
      const q = [];
      while (i < lines.length && lines[i].startsWith("> ")) { q.push(lines[i].slice(2).trim()); i++; }
      body.push(...callout(q)); continue;
    }
    if (/^\d+\.\s/.test(L)) {
      while (i < lines.length && /^\d+\.\s/.test(lines[i])) {
        body.push(new Paragraph({ numbering: { reference: "nums", level: 0 }, alignment: AlignmentType.JUSTIFIED, spacing: { after: 80, line: 340 }, children: runs(lines[i].replace(/^\d+\.\s/, "")) }));
        i++;
      }
      continue;
    }
    if (L.startsWith("- ")) {
      while (i < lines.length && lines[i].startsWith("- ")) {
        body.push(new Paragraph({ numbering: { reference: "bullets", level: 0 }, alignment: AlignmentType.JUSTIFIED, spacing: { after: 80, line: 340 }, children: runs(lines[i].slice(2)) }));
        i++;
      }
      continue;
    }
    if (fname === "refs.md" && /^\[\d+\]/.test(L)) {
      body.push(new Paragraph({ alignment: AlignmentType.LEFT, spacing: { after: 40, line: 250 }, indent: { left: 500, hanging: 500 }, children: runs(L, { size: 16 }) }));
      i++; continue;
    }
    // normal paragraph
    body.push(para(L, { indent: { firstLine: 420 } }));
    i++;
  }
}

function cover(title, sub, meta) {
  const out = [];
  out.push(new Paragraph({ spacing: { before: 2400 }, children: [] }));
  out.push(new Paragraph({ alignment: AlignmentType.LEFT, spacing: { after: 200 }, border: { bottom: { style: BorderStyle.SINGLE, size: 18, color: ACCENT, space: 8 } },
    children: [new TextRun({ text: "行业分析报告", font: fonts, size: 24, color: ACCENT, bold: true })] }));
  out.push(new Paragraph({ alignment: AlignmentType.LEFT, spacing: { before: 400, after: 200, line: 520 }, children: [new TextRun({ text: title, font: fonts, size: 48, bold: true, color: BLUE })] }));
  out.push(new Paragraph({ alignment: AlignmentType.LEFT, spacing: { after: 1800 }, children: [new TextRun({ text: sub, font: fonts, size: 26, color: GREY })] }));
  out.push(new Paragraph({ alignment: AlignmentType.LEFT, spacing: { after: 120 }, children: [new TextRun({ text: "研究重点：编程基础较弱、主要依靠自然语言进行开发的个人与小型研发团队，在维护已有网站、Web 应用和线上业务工具时的需求与困难", font: fonts, size: 20, color: GREY })] }));
  out.push(new Paragraph({ spacing: { before: 3200 }, children: [] }));
  for (const m of meta) out.push(new Paragraph({ alignment: AlignmentType.LEFT, spacing: { after: 80 }, children: [new TextRun({ text: m, font: fonts, size: 18, color: GREY })] }));
  out.push(new Paragraph({ alignment: AlignmentType.LEFT, spacing: { before: 200 }, children: [new TextRun({ text: "2026 年 10 月", font: fonts, size: 20, color: BLUE, bold: true })] }));
  out.push(new Paragraph({ children: [new PageBreak()] }));
  return out;
}

function tocBlock() {
  // static TOC built from toc_pages.json (two-pass); wrapped later into a TOC field by post-processing
  const out = [];
  out.push(new Paragraph({ alignment: AlignmentType.LEFT, spacing: { after: 240 }, children: [new TextRun({ text: "目录", font: fonts, size: 32, bold: true, color: BLUE })] }));
  out.push(new Paragraph({ children: [new TextRun({ text: "TOCSTART", size: 2, color: "FFFFFF" })] }));
  const entries = tocPages.entries || [];
  for (const e of entries) {
    const lvl = e.level;
    out.push(new Paragraph({
      spacing: { after: lvl === 1 ? 60 : 20, before: lvl === 1 ? 120 : 0, line: 280 },
      indent: { left: lvl === 1 ? 0 : (lvl === 2 ? 360 : 720) },
      tabStops: [{ type: TabStopType.RIGHT, position: TEXT_W, leader: "dot" }],
      children: [new TextRun({ text: e.text, font: fonts, size: lvl === 1 ? 21 : 19, bold: lvl === 1 }), new TextRun({ text: "\t" + e.page, font: fonts, size: lvl === 1 ? 21 : 19, bold: lvl === 1 })],
    }));
  }
  out.push(new Paragraph({ children: [new TextRun({ text: "TOCEND", size: 2, color: "FFFFFF" })] }));
  return out;
}

for (const f of FILES) parseFile(f);

const doc = new Document({
  creator: "行业分析课程研究",
  title: "面向独立开发者与小型研发团队的 AI 编程工具行业分析报告（2026）",
  styles: {
    default: { document: { run: { font: fonts, size: BODY_SIZE, color: "222222" }, paragraph: { spacing: { line: 340, lineRule: LineRuleType.AUTO } } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 34, bold: true, color: BLUE, font: fonts }, paragraph: { spacing: { before: 0, after: 360, line: 400 }, outlineLevel: 0, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: ACCENT, space: 6 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, color: BLUE, font: fonts }, paragraph: { spacing: { before: 320, after: 160, line: 360 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 22, bold: true, color: "2A5A9B", font: fonts }, paragraph: { spacing: { before: 200, after: 120, line: 340 }, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 600, hanging: 300 } } } }] },
      { reference: "nums", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 600, hanging: 360 } } } }] },
    ],
  },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MT, bottom: MB, left: ML, right: MR, header: 700, footer: 700 } }, titlePage: true },
    headers: {
      default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF", space: 4 } }, children: [new TextRun({ text: "面向独立开发者与小型研发团队的 AI 编程工具行业分析报告（2026）", font: fonts, size: 15, color: GREY })] })] }),
      first: new Header({ children: [new Paragraph({ children: [] })] }),
    },
    footers: {
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: fonts, size: 16, color: GREY })] })] }),
      first: new Footer({ children: [new Paragraph({ children: [] })] }),
    },
    children: body,
  }],
});

Packer.toBuffer(doc).then(buf => {
  const out = path.join(ROOT, "build", "report_raw.docx");
  fs.writeFileSync(out, buf);
  console.log("written", out, buf.length);
});
