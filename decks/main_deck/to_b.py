"""把主 deck（编辑式系统，45 页）转成方案 B 海报 + 背景层 E1–E5（47 页），落位见 skill/background-layers.md。
输入是改版前的编辑式 deck（git 3693220 及更早的 decks/main_deck/project），输出 B 版。
用法：python3 decks/main_deck/to_b.py <编辑式 deck 根目录> <输出根目录> tools/render/blobmap.txt
底图 /_blob id 为主 deck 工件中的上传资产，本地文件在 decks/main_deck/bg/。
"""
import re, sys, json, math, os

ORIG, OUT, BLOBMAP = sys.argv[1:4]
INK, PAPER, PANEL, RED, RED_T, GREY = "#111111", "#F2EFE6", "#F6F3EC", "#FF3B1F", "#C8301A", "#444444"
D_TXT, D_SUB, D_MUT, D_LINE = "#F2EFE6", "#C9C4B8", "#9A958A", "#3A3833"
SERIF = "'Noto Serif SC',Georgia,serif"
SANS = "'Noto Sans SC',Arial,sans-serif"
MONO = "'JetBrains Mono','Courier New',monospace"
BG_DOT = "/_blob/65ac61553383eb26e30adebf6b7554bf"
BG_ARR = "/_blob/de2a5a870fa4f3d7f1452e3db14efa14"
BG_BARS = "/_blob/45321e0ee08ecccf5f28452eef4b2279"
BG_SWE = "/_blob/36e5ca1312ae4ca1b1d01f7ca56c1760"
BG_NET = "/_blob/eaae01207e1f71e89791d34fd8ed34cb"

deck = json.load(open(f"{ORIG}/project/deck.json"))
order = list(deck["order"])
# background-layers.md 落位：E3 一句话结论页插在 s2-arr、s8-predictions 之前
order.insert(order.index("s2-arr"), "e3-arr")
order.insert(order.index("s8-predictions"), "e3-pred")
N = len(order)
blob2file = {}
for line in open(BLOBMAP):
    k, v = line.split()
    blob2file.setdefault(k, os.path.basename(v))


def src(sid):
    return open(f"{ORIG}/project/slides/{sid}.html").read()


def units(s):
    s = re.sub(r"<[^>]+>", "", s)
    return sum(0.55 if ord(c) < 128 else 1.0 for c in s)


def nlines(s, size, width):
    return max(1, math.ceil(units(s) * size / width))


def aside(t):
    return re.search(r"<aside>.*?</aside>", t, re.S).group(0)


def ps(t):
    """all <p ...>inner</p> as (style, inner)"""
    return re.findall(r'<p style="([^"]*)">(.*?)</p>', t, re.S)


def header(t):
    h = ps(t)[:2]
    return h[0][1], h[1][1]


def h2_inner(t):
    return re.search(r"<h2[^>]*>(.*?)</h2>", t, re.S).group(1)


def footer_parts(t):
    """the two pinned footer <p>s: source (left) and evidence/page (right)"""
    left = re.search(r'<p style="position:absolute;left:128px;bottom:64px[^"]*">(.*?)</p>', t, re.S)
    right = re.search(r'<p style="position:absolute;right:128px;bottom:64px[^"]*">(.*?)</p>', t, re.S)
    return (left.group(1) if left else ""), (right.group(1) if right else "")


def page_no(sid):
    return f"{order.index(sid) + 1} / {N}"


def right_label(r, sid, dark=False):
    m = re.search(r"证据强度\s*(\S+)", r)
    pn = page_no(sid)
    if not m:
        return pn
    lv = m.group(1)
    weak = "中" in lv or "弱" in lv
    col = (RED if dark else RED_T) if weak else (D_TXT if dark else INK)
    return f'<span style="color:{col}">证据 {lv}</span>　·　{pn}'


SEC_PAPER = f"background:{PAPER};color:{INK};font-family:{SANS};padding:64px 96px 160px;display:flex;flex-direction:column;gap:24px"


def topbar(l, r, dark=False):
    c = D_TXT if dark else INK
    p = f"font-family:{MONO};font-size:22px;line-height:1.4;color:{c};letter-spacing:2px"
    return (f'<div style="display:flex;justify-content:space-between;align-items:end;gap:48px;border-bottom:4px solid {c};padding:0 0 14px">'
            f'<p style="{p}">{l}</p><p style="{p};white-space:nowrap">{r}</p></div>')


def h2(inner, size=44, dark=False):
    return (f'<h2 style="font-family:{SERIF};font-size:{size}px;line-height:1.25;font-weight:900;'
            f'color:{D_TXT if dark else INK};width:1728px">{inner}</h2>')


def footer(left, right, dark=False):
    line = D_TXT if dark else INK
    sub = D_MUT if dark else GREY
    return (f'<div style="position:absolute;left:96px;bottom:56px;width:1728px;display:flex;justify-content:space-between;align-items:end;gap:48px;border-top:1px solid {line};padding:14px 0 0">'
            f'<p style="font-size:20px;line-height:1.4;color:{sub};width:1300px">{left}</p>'
            f'<p style="font-family:{MONO};font-size:20px;line-height:1.4;color:{line};white-space:nowrap">{right}</p></div>')


def footer_h(left):
    return 15 + nlines(left, 20, 1300) * 28


def restyle(body, dark=False):
    """map the old editorial palette/fonts onto B inside content blocks"""
    rep = [
        ("'IBM Plex Mono','Courier New',monospace", MONO),
        ("border-top:2px solid #1A1D22", f"border-top:4px solid {INK}"),
        ("border-top:1px solid #1A1D22", f"border-top:4px solid {INK}"),
        ("border-top:2px solid #B9462B", f"border-top:4px solid {RED}"),
        ("border-top:1px solid #B9462B", f"border-top:4px solid {RED}"),
        ("#1A1D22", INK), ("#5A5F66", GREY), ("#244B74", INK), ("#B9462B", RED_T), ("#8A867C", "#7A7568"),
        ("font-weight:600", "font-weight:900"),
    ]
    for a, b in rep:
        body = body.replace(a, b)
    return body


def section_open(sid, style):
    return f'<section id="{sid}" data-transition="fade" style="{style}">'


# ---------------------------------------------------------------- figure pages (B + E4)
def window(left, top, w, h, label, img_src, alt):
    out = []
    for i, (bg, bw) in enumerate([("#E3DED0", 2), ("#ECE8DD", 2)]):
        out.append(f'<div style="position:absolute;left:{left - 40 + 20 * i}px;top:{top - 40 + 20 * i}px;width:{w}px;height:{h}px;background:{bg};border:{bw}px solid {INK}"></div>')
    img_h = h - 6 - 46 - 24
    img_w = w - 6 - 40
    out.append(
        f'<div style="position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px;background:{PANEL};border:3px solid {INK};display:flex;flex-direction:column">'
        f'<div style="display:flex;align-items:center;gap:10px;height:46px;padding:0 20px;border-bottom:2px solid {INK}">'
        f'<div style="width:14px;height:14px;background:{RED}"></div><div style="width:14px;height:14px;background:{INK}"></div><div style="width:14px;height:14px;background:{INK}"></div>'
        f'<p style="font-family:{MONO};font-size:20px;color:{GREY};padding:0 0 0 14px">{label}</p></div>'
        f'<div style="display:flex;justify-content:center;padding:12px 20px">'
        f'<img src="{img_src}" alt="{alt}" style="width:{img_w}px;height:{img_h}px;object-fit:contain"></div></div>')
    return "\n".join(out)


def fig_page(sid):
    t = src(sid)
    lt, rt = header(t)
    hh = h2_inner(t)
    m = re.search(r'<img src="([^"]+)" alt="([^"]*)"', t)
    img, alt = m.group(1), m.group(2)
    fl, fr = footer_parts(t)
    fname = blob2file.get(img.split("/")[-1], "")
    label = f"{rt} · {fname}" if fname else rt
    h2_bottom = 64 + 49 + 24 + nlines(hh, 44, 1728) * 55
    front_top = h2_bottom + 28 + 40
    foot_top = 1080 - 56 - footer_h(fl)
    extra = ""
    left, w = 136, 1656
    if sid == "s2-bottomup":
        w = 1180
        side = re.search(r'<div style="flex:1;display:flex;flex-direction:column;gap:14px;border-top[^"]*">(.*?)</div>\n</div>', t, re.S).group(1)
        front_bottom = min(foot_top - 24, 944)
        extra = (f'<div style="position:absolute;left:{left + w + 48}px;top:{front_top}px;width:{1792 - left - w - 48}px;display:flex;flex-direction:column;gap:16px;border-top:4px solid {INK};padding:20px 0 0">'
                 f'{restyle(side)}</div>')
    elif sid in ("s5-case-replit", "s6-case-lovable"):
        cols = re.search(r'<div style="display:flex;gap:48px">\n(.*?)\n</div>\n<p style="position:absolute', t, re.S).group(1)
        front_bottom = front_top + 470
        extra = (f'<div style="position:absolute;left:96px;top:{front_bottom + 36}px;width:1696px;display:flex;gap:48px">'
                 f'{restyle(cols)}</div>')
    else:
        front_bottom = min(foot_top - 24, 944)
    h = front_bottom - front_top
    out = [section_open(sid, SEC_PAPER),
           window(left, front_top, w, h, label, img, alt),
           topbar(lt, rt), h2(hh)]
    if extra:
        out.append(extra)
    out += [footer(fl, right_label(fr, sid)), aside(t), "</section>"]
    return "\n".join(out)


# ---------------------------------------------------------------- table / text pages (B)
def text_page(sid):
    t = src(sid)
    lt, rt = header(t)
    hh = h2_inner(t)
    fl, fr = footer_parts(t)
    body = t.split("</h2>", 1)[1]
    body = re.split(r'\n<p style="position:absolute;left:128px;bottom:64px', body)[0].strip()
    body = restyle(body)
    body = body.replace('<table style="', f'<table style="border-top:4px solid {INK};border-bottom:4px solid {INK};')
    body = body.replace("width:1664px", "width:1728px")
    # table row numbers (predictions): serif red
    body = body.replace(f"font-family:{SERIF};color:{INK};font-size:30px", f"font-family:{SERIF};color:{RED_T};font-size:30px;font-weight:900")
    right = right_label(fr, sid) if fr else page_no(sid)
    rt = rt or ""
    out = [section_open(sid, SEC_PAPER), topbar(lt, rt or "AI 编程工具行业调研 · 2026"), h2(hh), body,
           footer(fl, right), aside(t), "</section>"]
    return "\n".join(out)


def findings_page(sid):
    t = src(sid)
    lt, _ = header(t)
    hh = h2_inner(t)
    fl, fr = footer_parts(t)
    rows = re.findall(r'<div style="display:flex;gap:32px;align-items:start;[^"]*">(.*?)</div></div>?(?=\n)', t)
    rows = re.findall(r'<div style="display:flex;gap:32px;align-items:start;[^"]*"><p[^>]*>(.*?)</p><div[^>]*><p[^>]*>(.*?)</p><p[^>]*>(.*?)</p></div><p[^>]*>(.*?)</p></div>', t)
    out = [section_open(sid, SEC_PAPER), topbar(lt, "AI 编程工具行业调研 · 2026"), h2(hh, 40),
           '<div style="display:flex;flex-direction:column">']
    for i, (num, title, det, lv) in enumerate(rows):
        weak = "中" in lv or "弱" in lv
        bb = f";border-bottom:2px solid {INK}" if i == len(rows) - 1 else ""
        out.append(
            f'<div style="display:flex;gap:32px;align-items:start;border-top:2px solid {INK}{bb};padding:14px 0">'
            f'<p style="font-family:{SERIF};font-size:60px;line-height:0.95;font-weight:900;color:{RED};width:96px">{num}</p>'
            f'<div style="flex:1;display:flex;flex-direction:column;gap:4px">'
            f'<p style="font-family:{SERIF};font-size:28px;line-height:1.3;font-weight:900;color:{INK}">{title}</p>'
            f'<p style="font-size:21px;line-height:1.45;color:{GREY}">{det}</p></div>'
            f'<p style="font-family:{MONO};font-size:20px;color:{RED_T if weak else INK};width:110px;text-align:right;letter-spacing:2px">{lv}</p></div>')
    out += ["</div>", footer(fl, page_no(sid)), aside(t), "</section>"]
    return "\n".join(out)


# ---------------------------------------------------------------- dividers (B + E1)
def divider(sid):
    t = src(sid)
    p = ps(t)
    chap, num = p[0][1], p[1][1]
    title = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S).group(1)
    cols = re.findall(r'<p style="[^"]*letter-spacing:2px">(事实|机制|判断)</p><p style="[^"]*">(.*?)</p>', t)
    col_html = "".join(
        f'<div style="flex:1;display:flex;flex-direction:column;gap:10px">'
        f'<p style="font-family:{MONO};font-size:20px;color:{RED_T if k == "判断" else INK};letter-spacing:2px">{k}</p>'
        f'<p style="font-size:21px;line-height:1.55;color:{INK}">{v}</p></div>' for k, v in cols)
    lab = f"font-family:{MONO};font-size:22px;line-height:1.4;color:{INK};letter-spacing:2px"
    return "\n".join([
        section_open(sid, f"background:{PAPER};color:{INK};font-family:{SANS}"),
        f'<img src="{BG_DOT}" alt="" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover">',
        f'<div style="position:absolute;left:128px;top:120px;width:1664px;height:832px;display:flex;flex-direction:column;justify-content:space-between">',
        f'<div style="display:flex;justify-content:space-between;border-bottom:4px solid {INK};padding:0 0 14px">'
        f'<p style="{lab}">{chap}</p><p style="{lab}">AI 编程工具行业调研 · 2026</p><p style="{lab}">{page_no(sid)}</p></div>',
        f'<div style="display:flex;align-items:end;gap:56px">'
        f'<p style="font-family:{SERIF};font-size:360px;line-height:0.85;font-weight:900;color:{INK};letter-spacing:-16px">{num}</p>'
        f'<h1 style="font-family:{SERIF};font-size:76px;line-height:1.15;font-weight:900;color:{RED};width:900px;padding:0 0 28px">{title}</h1></div>',
        f'<div style="display:flex;gap:48px;border-top:2px solid {INK};padding:22px 0 0">{col_html}</div>',
        "</div>", aside(t), "</section>"])


# ---------------------------------------------------------------- hand-built pages
def cover():
    t = src("cover")
    lab = f"font-family:{MONO};font-size:22px;line-height:1.4;color:{INK};letter-spacing:2px"
    meta = f"font-family:{MONO};font-size:20px;color:{INK}"
    return "\n".join([
        section_open("cover", f"background:{PAPER};color:{INK};font-family:{SANS}"),
        f'<img src="{BG_DOT}" alt="" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover">',
        f'<div style="position:absolute;left:128px;top:120px;width:1664px;height:832px;display:flex;flex-direction:column;justify-content:space-between">',
        f'<div style="display:flex;justify-content:space-between;border-bottom:4px solid {INK};padding:0 0 14px">'
        f'<p style="{lab}">行业分析报告</p><p style="{lab}">研究阶段 · 行业分析</p><p style="{lab}">2026 · 10</p></div>',
        f'<div style="display:flex;flex-direction:column;gap:36px">',
        f'<h1 style="font-family:{SERIF};font-size:120px;line-height:1.08;font-weight:900;color:{INK};letter-spacing:-2px;width:1664px">面向独立开发者与<br>小型研发团队的<br><span style="color:{RED}">AI 编程工具行业调研</span></h1>',
        f'<p style="font-size:28px;line-height:1.55;color:{INK};width:1240px">研究重点：编程基础较弱、主要依靠自然语言开发的个人与小型团队，在维护已有网站、Web 应用与线上业务工具时的需求与困难</p>',
        "</div>",
        f'<div style="display:flex;justify-content:space-between;border-top:1px solid {INK};padding:14px 0 0">'
        f'<p style="{meta}">资料检索截止 2026-10-14</p><p style="{meta}">产品与价格核查 2026-10-14</p><p style="{meta}">基于公开资料的综合研究 · 未做一手访谈与统一实测</p></div>',
        "</div>", aside(t), "</section>"])


def stats():
    t = src("stats")
    cells = [
        ("调研 · 2025", "55%", "美国企业部门级生成式 AI 支出中编程的占比（Menlo）"),
        ("预测 · 2026", "11.73 亿元", "中国 AI 编程市场预测；2025 年为 3.99 亿元（IDC）"),
        ("研究", "10–18%", "前沿模型在商业私有仓库任务上的通过率；公开基准为 70% 以上"),
        ("调查 · 2026", "65.5%", "Claude Code 过去一年使用率，居编程智能体首位（SO 2026）"),
        ("调查 · 2025", "46%", "开发者不信任 AI 输出的准确性（Stack Overflow 2025）"),
        ("研究", "36%", "vibe coding 从业者记录中跳过质量保证的比例（n=518）"),
    ]
    cell_html = "".join(
        f'<div style="display:flex;flex-direction:column;gap:8px;border-top:3px solid {INK};padding:16px 0 0">'
        f'<p style="font-family:{MONO};font-size:20px;color:{GREY};letter-spacing:2px">{a}</p>'
        f'<p style="font-family:{SERIF};font-size:60px;line-height:1;font-weight:900;color:{INK}">{b}</p>'
        f'<p style="font-size:20px;line-height:1.45;color:{GREY}">{c}</p></div>' for a, b, c in cells)
    lab = f"font-family:{MONO};font-size:22px;line-height:1.4;color:{PAPER};letter-spacing:2px"
    return "\n".join([
        section_open("stats", f"background:{PAPER};color:{INK};font-family:{SANS};padding:0;display:flex;flex-direction:column"),
        f'<div style="height:440px;background:{RED};display:flex;flex-direction:column;justify-content:space-between;padding:64px 96px 40px">',
        f'<div style="display:flex;justify-content:space-between;border-bottom:4px solid {PAPER};padding:0 0 14px">'
        f'<p style="{lab}">执行摘要 — 关键数字</p><p style="{lab}">计算 · 2026 年年中</p></div>',
        f'<div style="display:flex;align-items:end;justify-content:space-between;gap:48px">'
        f'<p style="font-family:{SERIF};font-size:270px;line-height:0.9;font-weight:900;color:{PAPER};letter-spacing:-8px">≈87</p>'
        f'<p style="font-family:{SERIF};font-size:72px;line-height:1;font-weight:900;color:{PAPER};padding:0 0 22px">亿美元</p>'
        f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;padding:0 0 18px">'
        f'<p style="font-family:{SERIF};font-size:30px;line-height:1.45;font-weight:900;color:{PAPER}">六家头部厂商年化收入合计（研究者自下而上计算）</p>'
        f'<p style="font-size:24px;line-height:1.5;color:{PAPER}">已高于最宽口径机构对 2025 年全球市场的估计：81.4 亿美元（MarketsandMarkets，估计，含编程 API）</p></div></div>',
        "</div>",
        f'<div style="flex:1;display:flex;flex-direction:column;gap:22px;padding:36px 96px 120px">',
        f'<h2 style="font-family:{SERIF};font-size:40px;line-height:1.25;font-weight:900;color:{INK}">规模口径相差两个数量级；使用已普及，但信任有条件</h2>',
        f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:28px 48px">{cell_html}</div>',
        "</div>",
        footer("性质：估计 / 计算 / 调研 / 预测 / 调查 / 研究 · 口径不同，不可相加 · 来源 [1][5][8][14][16][101][131]", page_no("stats")),
        aside(t), "</section>"])


def dark_page(sid, bg, label, title, cols, bottom, foot):
    """E3: ink page over a dimmed chart trace; all text in one pinned container"""
    lab = f"font-family:{MONO};font-size:22px;line-height:1.4;color:{D_TXT};letter-spacing:2px"
    col_html = []
    for (k, head, body, accent) in cols:
        c = RED if accent else D_TXT
        hd = f'<h3 style="font-family:{SERIF};font-size:34px;line-height:1.25;font-weight:900;color:{D_TXT}">{head}</h3>' if head else ""
        col_html.append(
            f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;border-top:4px solid {c};padding:18px 0 0">'
            f'<p style="font-family:{MONO};font-size:20px;color:{c};letter-spacing:2px">{k}</p>{hd}'
            f'<p style="font-size:22px;line-height:1.65;color:{D_SUB}">{body}</p></div>')
    parts = [
        section_open(sid, f"background:{INK};color:{D_TXT};font-family:{SANS}"),
        (f'<img src="{bg}" alt="" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover">' if bg else ""),
        f'<div style="position:absolute;left:96px;top:64px;width:1728px;height:840px;display:flex;flex-direction:column;justify-content:space-between;gap:32px">',
        f'<div style="display:flex;flex-direction:column;gap:24px">',
        f'<div style="display:flex;justify-content:space-between;border-bottom:4px solid {D_TXT};padding:0 0 14px"><p style="{lab}">{label}</p><p style="{lab}">{page_no(sid)}</p></div>',
        h2(title, 44, dark=True), "</div>",
        f'<div style="display:flex;gap:48px">{"".join(col_html)}</div>']
    if bottom:
        k, body = bottom
        parts.append(f'<div style="display:flex;flex-direction:column;gap:12px;border-top:4px solid {RED};padding:18px 0 0">'
                     f'<p style="font-family:{MONO};font-size:20px;color:{RED};letter-spacing:2px">{k}</p>'
                     f'<p style="font-size:22px;line-height:1.6;color:{D_SUB}">{body}</p></div>')
    parts += ["</div>", footer(foot, page_no(sid), dark=True), aside(src(sid)), "</section>"]
    return "\n".join(parts)


def risks():
    t = src("risks")
    h3s = re.findall(r"<h3[^>]*>(.*?)</h3>\n<p[^>]*>(.*?)</p>", t)
    bottom = re.findall(r'<p style="font-size:23px;line-height:1.6;color:#C9D3DE">(.*?)</p>', t)[-1]
    cols = [(f"0{i + 1}", h, b, False) for i, (h, b) in enumerate(h3s)]
    return dark_page("risks", None, "执行摘要 — 三项风险与本报告不知道的事", h2_inner(t), cols,
                     ("本报告不知道的事 — 无可靠公开数据", bottom), "详见第八章风险矩阵与证据强度表")


def method():
    t = src("method")
    blocks = re.findall(r'letter-spacing:2px">(资料类型|处理规则|主要限制)</p>\n<p[^>]*>(.*?)</p>', t)
    cols = [(k, "", v, k == "主要限制") for k, v in blocks]
    fl, _ = footer_parts(t)
    return dark_page("method", None, "研究方法、资料类型与主要限制", h2_inner(t), cols, None, fl)


# ---------------------------------------------------------------- E3 conclusion pages (new)
E3 = {
    "e3-arr": dict(bg=BG_ARR, label="02 — 行业发展与市场规模", big="40×",
                   title="Cursor 约 17 个月从 1 亿美元增至 40 亿美元",
                   cols=["Claude Code 25 亿（匿名信源）、Cognition 9 亿、Lovable 6 亿、Replit 5.25 亿：六家年化合计约 87 亿美元。",
                         "增长来自企业采购、智能体式用量与非技术用户三条线；限制是模型推理成本与算力容量。"],
                   src="资料来源：Cursor [28][30] · Anthropic [32][34] · Cognition [41] · Lovable [36][37] · Replit [38]；多为公司自述或媒体援引的匿名信源", lv="中",
                   note="E3 一句话结论页：底纹是下一页图 2-4 的五条年化收入走势线，去掉坐标与文字后压暗；真正的数据图在下一页正常展示。"),
    "e3-pred": dict(bg=BG_SWE, label="08 — 趋势、风险与可检验判断", big="95%",
                    title="两年里 SWE-bench Verified 顶分从 33% 升到 95%，可验证性没有跟上",
                    cols=["公开基准顶分 2024-06 为 33.4%，2026-06 为 95.0%（厂商自报）；商业私有仓库任务的通过率仍只有 10–18%。",
                          "46% 的开发者不信任 AI 输出。生成能力增长快于可验证性增长，是后面 8 项可检验判断的共同前提。"],
                    src="资料来源：SWE-bench Verified 厂商自报 [98][99][100]、SWE-bench Pro [101]；信任数据见执行摘要关键数字页", lv="中",
                    note="E3 一句话结论页：底纹是图 3-3 的 SWE-bench Verified 顶分走势线与 Pro 公开集走势线，去字压暗。这一页把第三章的能力曲线和第五章的信任数据接起来，引出第八章的判断表。"),
}


def e3_page(sid):
    c = E3[sid]
    lab = f"font-family:{MONO};font-size:22px;line-height:1.4;color:{D_TXT};letter-spacing:2px"
    cols = "".join(f'<p style="font-size:22px;line-height:1.6;color:{D_SUB};width:520px">{x}</p>' for x in c["cols"])
    return "\n".join([
        section_open(sid, f"background:{INK};color:{D_TXT};font-family:{SANS}"),
        f'<img src="{c["bg"]}" alt="" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover">',
        f'<div style="position:absolute;left:96px;top:64px;width:1728px;height:840px;display:flex;flex-direction:column;justify-content:space-between">',
        f'<div style="display:flex;justify-content:space-between;border-bottom:4px solid {D_TXT};padding:0 0 14px"><p style="{lab}">{c["label"]}</p><p style="{lab}">{page_no(sid)}</p></div>',
        f'<div style="display:flex;flex-direction:column;gap:24px;width:1100px">',
        f'<p style="font-family:{SERIF};font-size:200px;line-height:1;font-weight:900;color:{D_TXT}">{c["big"]}</p>',
        f'<h2 style="font-family:{SERIF};font-size:48px;line-height:1.3;font-weight:900;color:{D_TXT}">{c["title"]}</h2>',
        f'<div style="display:flex;gap:48px;border-top:1px solid {D_LINE};padding:20px 0 0">{cols}</div>',
        "</div></div>",
        footer(c["src"], f'<span style="color:{RED}">证据 {c["lv"]}</span>　·　{page_no(sid)}', dark=True),
        f'<aside>{c["note"]}</aside>', "</section>"])


# ---------------------------------------------------------------- E2 relation pages (network backdrop replaces the diagram)
NODES = [(1040, 300), (1040, 540), (1040, 780), (1700, 330), (1700, 540), (1700, 750), (1380, 220), (1380, 860)]
E2 = {
    "s4-chain": dict(hub="中游：工具与平台",
                     labels=["闭源模型厂商（也自营）", "开源模型 / 自研基座", "算力与云", "专业开发者", "企业采购", "低基础用户",
                             "交付接口：PR · MCP · BaaS", "断供：Windsurf 2025-06、Cursor 2026"],
                     body="上游是模型与算力云，三家闭源模型厂商同时在中游自营产品；中游五类工具与平台通过 GitHub 分支 / PR、MCP、BaaS 与平台一键发布交付给下游。上游不只是供应商——这是供应商议价能力强的根本原因。"),
    "s6-arch": dict(hub="用户的代码仓库",
                    labels=["IDE 内嵌助手", "AI 原生 IDE", "终端 / CLI 智能体", "云端异步智能体", "一体化应用平台", "验证：同一智能体自测",
                            "逃生通道：Git 分支 / PR", "风险：数据库不随版本回滚"],
                    body="五类架构的差别在执行环境、仓库方式与验证闭环。基于用户 Git 仓库的工具可随时换工具；一体化平台的项目主要存在于平台内，多数不能导入已有仓库。验证闭环已普及，但由同一个智能体报告。"),
}


def e2_page(sid):
    t = src(sid); c = E2[sid]
    lt, rt = header(t)
    fl, fr = footer_parts(t)
    fl = fl.split("；")[0]   # 旧图的图例说明不再适用
    out = [section_open(sid, SEC_PAPER),
           f'<img src="{BG_NET}" alt="" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover">',
           # 全出血底图上的正文整体装进一个绝对定位容器，否则会被底图盖住
           f'<div style="position:absolute;left:96px;top:64px;width:1728px;height:840px;display:flex;flex-direction:column;gap:24px">',
           topbar(lt, rt),
           f'<div style="display:flex;flex-direction:column;gap:28px;width:820px">',
           f'<h2 style="font-family:{SERIF};font-size:44px;line-height:1.25;font-weight:900;color:{INK}">{h2_inner(t)}</h2>',
           f'<p style="font-size:24px;line-height:1.6;color:{GREY};border-top:4px solid {INK};padding:20px 0 0">{c["body"]}</p></div></div>']
    for i, ((x, y), lb) in enumerate(zip(NODES, c["labels"])):
        col = RED_T if i == 7 else INK
        if i == 7:   # bottom node: one wide line under the node, clear of the right-column labels
            out.append(f'<p style="position:absolute;left:{x - 180}px;top:{y + 50}px;width:360px;text-align:center;font-family:{MONO};font-size:20px;line-height:1.3;color:{col}">{lb}</p>')
        elif i == 6:   # top node: label to the right, keeps the hub line clear
            out.append(f'<p style="position:absolute;left:{x + 56}px;top:{y - 16}px;width:300px;font-family:{MONO};font-size:20px;line-height:1.3;color:{col}">{lb}</p>')
        else:
            out.append(f'<p style="position:absolute;left:{x - 92}px;top:{y + 50}px;width:184px;text-align:center;font-family:{MONO};font-size:20px;line-height:1.3;color:{col}">{lb}</p>')
    out.append(f'<p style="position:absolute;left:1316px;top:510px;width:128px;text-align:center;font-family:{SERIF};font-size:22px;line-height:1.3;font-weight:900;color:{INK}">{c["hub"]}</p>')
    out += [footer(fl, right_label(fr, sid)), aside(t), "</section>"]
    return "\n".join(out)


# ---------------------------------------------------------------- run
os.makedirs(f"{OUT}/project/slides", exist_ok=True)
FIG = [s for s in order if s not in E3 and "<img" in src(s)]
TEXT = ["def", "s2-sources", "s8-predictions", "s8-predictions2", "s8-evidence", "s8-evidence2"]
done = {}
for s in order:
    if s in E3: h = e3_page(s)
    elif s in E2: h = e2_page(s)
    elif s == "cover": h = cover()
    elif s == "stats": h = stats()
    elif s == "risks": h = risks()
    elif s == "method": h = method()
    elif s.startswith("findings"): h = findings_page(s)
    elif re.fullmatch(r"d\d", s): h = divider(s)
    elif s in FIG: h = fig_page(s)
    elif s in TEXT: h = text_page(s)
    else: raise SystemExit(f"unhandled {s}")
    open(f"{OUT}/project/slides/{s}.html", "w").write(h + "\n")
    done[s] = h
print(len(done), "slides")
