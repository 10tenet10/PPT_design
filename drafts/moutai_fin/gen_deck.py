# -*- coding: utf-8 -*-
"""生成贵州茅台经营分析 deck（编辑式 + E1/E3/E4/E5）：deck.json + slides/*.html。
运行：python3 drafts/moutai_fin/gen_deck.py  → drafts/moutai_fin/deck/project/"""
import os, re, json, html
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deck", "project")
os.makedirs(os.path.join(OUT, "slides"), exist_ok=True)

PAPER, INK, GREY, LINE, ACC, WARM, DEEP = "#F6F3EC", "#1A1D22", "#5A5F66", "#D6D2C8", "#244B74", "#B9462B", "#15212E"
SERIF = "'Noto Serif SC',Georgia,serif"; SANS = "'Noto Sans SC',Arial,sans-serif"; MONO = "'IBM Plex Mono','Courier New',monospace"
BLOB = {"fig1_2": "78be24f5a5034e9cbacac46f38c6da55", "fig2_1": "8044119b8e67163f9912f5b20b571b2b", "fig2_2": "f01abf57592908ca087a4199f3ab0078",
        "fig2_3": "7050730a4210418f4cc94397a8bf2ca6", "fig3_1": "35444c461165b8f158f7ac7ea6b9e586", "fig3_2": "14482d67397df4ae368a4ab72a87c926",
        "fig4_1": "9cee758fa5d312eb261235eb473d400f", "fig4_2": "08ca6c160bcc9ae1759512ae46df97c9", "fig5_2": "a1f0bcb72077346c7e64176c419c501c",
        "fig6_2": "fe1dc065bd9fe316135a43fcf58c33b6", "fig6_3": "dfd4a8b22bdac60b65ecd2b15dfca654",
        "e3rev": "51b2a7a6b67a378265e31ec4f8706fbd", "e3con": "ada2a6f41fb3c0af37df1df16cd83015", "dot": "b21dd54deb5a1498552ca212f7cb8915"}

def mono(t, color=GREY, size=20, extra=""):
    return f'<p style="font-family:{MONO};font-size:{size}px;color:{color};letter-spacing:2px;{extra}">{t}</p>'
def topbar(left, right, color=GREY):
    return f'<div style="display:flex;justify-content:space-between;align-items:center">{mono(left, color)}{mono(right, color)}</div>'
def hr(color=LINE):
    return f'<hr style="width:1664px;border-top:1px solid {color}">'
def h2(t, color=INK, size=46):
    return f'<h2 style="font-family:{SERIF};font-size:{size}px;line-height:1.3;font-weight:600;color:{color};width:1560px">{t}</h2>'
def footer(src, right, n, total, color=GREY, rcolor=GREY):
    return (f'<p style="position:absolute;left:128px;bottom:64px;width:1300px;font-size:20px;line-height:1.4;color:{color}">{src}</p>'
            f'<p style="position:absolute;right:128px;bottom:64px;font-family:{MONO};font-size:20px;color:{rcolor};letter-spacing:1px">{right}　·　{n} / {total}</p>')
def strength(s):
    return f'证据强度 <span style="color:{WARM}">{s}</span>' if s in ("中", "弱") else f'证据强度 {s}'
def aside(t):
    return f'<aside>{html.escape(t)}</aside>' if t else ''
def section(sid, body, bg=PAPER, color=INK, pad="96px 128px 160px", extra="display:flex;flex-direction:column;gap:24px"):
    return f'<section id="{sid}" data-transition="fade" style="background:{bg};color:{color};font-family:{SANS};padding:{pad};{extra}">\n{body}\n</section>\n'

def _fix_aside(h):
    m = re.search(r'</section>\n(<aside>.*?</aside>)$', h, re.S)
    return h[:m.start()] + m.group(1) + '\n</section>\n' if m else h

PAGES = []  # (id, builder) ; builder(n, total) -> html
def add(sid, fn): PAGES.append((sid, fn))

# ---------- 封面（E1） ----------
def cover(n, total):
    body = (f'<img src="/_blob/{BLOB["dot"]}" alt="" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover">'
            f'<div style="position:absolute;left:128px;top:128px;width:1664px;height:792px;display:flex;flex-direction:column;justify-content:space-between">'
            f'<div style="display:flex;justify-content:space-between;align-items:center">{mono("财务与经营分析　2026 年 11 月")}{mono("方向 4 · 管理学案例作业")}</div>'
            f'<div style="display:flex;flex-direction:column;gap:40px"><hr style="width:96px;border-top:3px solid {ACC}">'
            f'<h1 style="font-family:{SERIF};font-size:88px;line-height:1.25;font-weight:600;color:{INK};width:1500px">贵州茅台经营分析：<br>增长停摆后的现金、渠道与定价</h1>'
            f'<p style="font-size:28px;line-height:1.6;color:{GREY};width:1300px">对象：贵州茅台酒股份有限公司（600519.SH），合并报表口径，FY2021–FY2025 年报与 2026 年前三季度；同业对照：五粮液、泸州老窖、山西汾酒</p></div>'
            f'<div style="display:flex;gap:96px;border-top:1px solid {LINE};padding:24px 0 0">{mono("取证截止　2026-11-05", size=19)}{mono("年报、季报与公告均为原文", size=19)}{mono("七类证据 · 三级强度 · 无自采数据", size=19)}</div></div>')
    return section("cover", body, pad="0", extra="") + aside("封面。对象是上市公司合并报表，不含集团的习酒、文旅等业务。所有三表数字来自年报与季报原文；批价、治理事件来自媒体转引，强度标中。")
add("cover", cover)

# ---------- 方法页（深底） ----------
def method(n, total):
    col = lambda lab, txt, c=ACC: (f'<div style="flex:1;display:flex;flex-direction:column;gap:14px;border-top:1px solid #2E4256;padding:24px 0 0">{mono(lab, "#9FB0C2", 19)}'
                                   f'<p style="font-size:23px;line-height:1.7;color:#C9D3DE">{txt}</p></div>')
    body = (topbar("方法与限制", "", "#9FB0C2") + hr("#2E4256") +
            h2("七类证据、三级强度；三表数字全部来自年报与季报原文，批价与治理事件为媒体转引", PAPER) +
            '<div style="display:flex;gap:48px;flex:1">' +
            col("证据七类", "实际值 / 自采数据 / 估计 / 预测 / 模型输出 / 厂商自述 / 推断<br>原文直接计算的比率标「实际值（计算）」并写算式<br>本报告无自采数据") +
            col("口径", "营业总收入 = 营业收入 + 财务公司利息收入，两者分列<br>年报经营目标按营业总收入，季报首页按营业收入<br>现金流与负债率另列「剔除财务公司」口径") +
            col("主要限制", "上交所静态站有机器人拦截，原文取自公司官网与巨潮资讯<br>2021 年营业总收入、2026-03 调价公告只开到转引，标中<br>批价来自今日酒价经媒体转引，不是公司披露数据<br>2026 年数据为未审计季报", ) +
            '</div>' + footer("规格：industry-research-deck 主 skill + management-topics R1–R8；建议只在第八章出现，每条带依据与翻转条件", "方法", n, total, "#9FB0C2", "#9FB0C2"))
    return section("method", body, DEEP, PAPER) + aside("方法页。七类证据来自 management-topics R2。模型输出页（第六章）的每个输入在页脚列来源编号，强度取最弱输入。")
add("method", method)

# ---------- 分隔页（E1 + 幽灵数字） ----------
def divider(sid, num, title, facts):
    def fn(n, total):
        cols = "".join(f'<div style="flex:1;display:flex;flex-direction:column;gap:10px">{mono(k, ACC, 19)}<p style="font-size:23px;line-height:1.6;color:{INK}">{v}</p></div>' for k, v in facts)
        body = (f'<img src="/_blob/{BLOB["dot"]}" alt="" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover">'
                f'<p style="position:absolute;right:112px;top:96px;width:760px;text-align:right;font-family:{SERIF};font-size:400px;line-height:1;font-weight:600;color:#E7E2D6">{num}</p>'
                f'<div style="position:absolute;left:128px;top:128px;width:1664px;height:792px;display:flex;flex-direction:column;justify-content:space-between">'
                f'{mono("第" + "一二三四五六七八"[int(num) - 1] + "章")}'
                f'<div style="display:flex;align-items:end;gap:48px"><p style="font-family:{SERIF};font-size:260px;line-height:0.9;font-weight:400;color:{ACC}">{num}</p>'
                f'<h1 style="font-family:{SERIF};font-size:64px;line-height:1.2;font-weight:600;color:{INK};padding:0 0 24px">{title}</h1></div>'
                f'<div style="display:flex;gap:48px;border-top:1px solid {INK};padding:28px 0 0">{cols}</div></div>')
        return section(sid, body, pad="0", extra="") + aside(f"第{num}章分隔页：事实 / 机制 / 判断三行与正文 KEYPOINTS 相同。")
    add(sid, fn)

# ---------- 图页（E4 全宽三层窗口，编辑式配色） ----------
def figure(sid, chap, figlab, title, key, alt, src, stren, note, imgw=1610, imgh=520):
    def fn(n, total):
        win = (f'<div style="position:absolute;left:72px;top:296px;width:1656px;height:584px;background:#ECE8DD;border:1px solid {LINE};border-radius:14px"></div>'
               f'<div style="position:absolute;left:104px;top:328px;width:1656px;height:584px;background:#F2EEE5;border:1px solid {LINE};border-radius:14px"></div>'
               f'<div style="position:absolute;left:136px;top:360px;width:1656px;height:584px;background:#FFFFFF;border:1px solid {LINE};border-radius:14px;display:flex;flex-direction:column">'
               f'<div style="display:flex;align-items:center;gap:10px;height:40px;padding:0 20px;border-bottom:1px solid {LINE}"><div style="width:12px;height:12px;border-radius:50%;background:{ACC}"></div><div style="width:12px;height:12px;border-radius:50%;background:{LINE}"></div><div style="width:12px;height:12px;border-radius:50%;background:{LINE}"></div>{mono(figlab + " · " + key + ".png", GREY, 18, "padding:0 0 0 14px")}</div>'
               f'<div style="display:flex;justify-content:center;padding:10px 20px"><img src="/_blob/{BLOB[key]}" alt="{alt}" style="width:{imgw}px;height:{imgh}px;object-fit:contain"></div></div>')
        body = win + topbar(chap, figlab) + hr() + h2(title) + footer("资料来源：" + src, strength(stren), n, total)
        return section(sid, body) + aside(note)
    add(sid, fn)

# ---------- 表格页 ----------
def table_page(sid, chap, lab, title, cols, rows, src, stren, note, fs=26, widths=None, warm_rows=()):
    def fn(n, total):
        ws = widths or [round(100 / len(cols))] * len(cols)
        head = "".join(f'<th style="width:{w}%;text-align:left;font-weight:600;color:{INK}">{c}</th>' for c, w in zip(cols, ws))
        trs = ""
        for i, r in enumerate(rows):
            bg = ' background:#F0ECE3' if i % 2 else ''
            tds = "".join(f'<td style="color:{WARM if (i in warm_rows and j > 0) else INK}">{c}</td>' for j, c in enumerate(r))
            trs += f'<tr style="{bg.strip()}">{tds}</tr>'
        tbl = f'<table style="font-size:{fs}px;line-height:1.35;color:{INK};border:1px solid {LINE};padding:16px 18px"><tr>{head}</tr>{trs}</table>'
        body = topbar(chap, lab) + hr() + h2(title) + tbl + footer("资料来源：" + src, strength(stren), n, total)
        return section(sid, body) + aside(note)
    add(sid, fn)

# ---------- 关键数字页（E5 上下色块） ----------
def stats(n, total):
    cells = [("823.20 亿元", "归母净利润，−4.53%；扣非 822.93 亿元", "实际值"), ("615.22 亿元", "经营活动现金流，−33.46%；含财务公司存款变动 −50.99 亿元", "实际值"),
             ("16.4%", "资产负债率（含吸收存款 180.38 亿元）；2026 年 9 月末 11.9%", "实际值（计算）"), ("711.53 亿元", "现金分红 650.33 + 回购 61.20，占归母净利润 86.43%", "实际值")]
    grid = "".join(f'<div style="display:flex;flex-direction:column;gap:8px;border-top:1px solid {LINE};padding:18px 0 0"><p style="font-family:{SERIF};font-size:56px;line-height:1.1;font-weight:600;color:{INK}">{a}</p><p style="font-size:21px;line-height:1.5;color:{GREY}">{b}</p>{mono(c, ACC, 18)}</div>' for a, b, c in cells)
    top = (f'<div style="height:560px;background:{ACC};display:flex;flex-direction:column;justify-content:space-between;padding:96px 128px 48px">'
           f'<div style="display:flex;justify-content:space-between;align-items:center">{mono("01 — 公司与业务边界 · 关键数字", "#C9D3DE")}{mono("2025 年年度报告", "#C9D3DE")}</div>'
           f'<div style="display:flex;align-items:end;gap:40px"><p style="font-family:{SERIF};font-size:300px;line-height:0.9;font-weight:600;color:{PAPER};letter-spacing:-6px">1720.54</p>'
           f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;padding:0 0 22px"><p style="font-family:{SERIF};font-size:30px;line-height:1.4;font-weight:600;color:{PAPER}">亿元 · 2025 年营业总收入，同比 −1.20%，上市以来首次年度负增长</p>'
           f'<p style="font-size:24px;line-height:1.5;color:#C9D3DE">营业收入 1688.38 亿元；差额 32.16 亿元是并表的集团财务公司利息收入。酒类收入占营业收入 99.96%。</p></div></div></div>')
    bottom = (f'<div style="flex:1;display:flex;flex-direction:column;gap:20px;padding:36px 128px 120px"><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:28px 48px">{grid}</div></div>')
    body = top + bottom + footer("资料来源：贵州茅台 2025 年年度报告 [1]、2025 年度权益分派实施公告 [9]。四格口径不同，不可相加", strength("强"), n, total)
    return section("s1-stats", body, pad="0", extra="display:flex;flex-direction:column") + aside("关键数字页。营业总收入含利息收入；经营现金流降幅中 161.59 亿元来自财务公司存款净额的两年差；分红口径含 2025 年中期 300.01 亿元与年末 350.33 亿元。")
add_stats = lambda: add("s1-stats", stats)

# ---------- E3 结论页 ----------
def e3(sid, chap, key, big, title, left, right, labels, years, src, stren, note):
    def fn(n, total):
        labs = "".join(f'<p style="position:absolute;left:{x}px;top:{y}px;width:{w}px;text-align:{ta};font-family:{MONO};font-size:20px;line-height:1.2;color:#AEB4BD;letter-spacing:1px">{t}</p>' for t, x, y, w, ta in labels)
        yrs = "".join(f'<p style="position:absolute;left:{x - 50}px;top:532px;width:100px;text-align:center;font-family:{MONO};font-size:20px;color:#8A93A0">{t}</p>' for t, x in years)
        body = (f'<img src="/_blob/{BLOB[key]}" alt="" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover">' + labs + yrs +
                f'<div style="position:absolute;left:96px;top:64px;width:1728px;height:840px;display:flex;flex-direction:column;justify-content:space-between">'
                f'<div style="display:flex;justify-content:space-between;align-items:center">{mono(chap, "#AEB4BD")}{mono("一句话结论", "#AEB4BD")}</div>'
                f'<div style="display:flex;flex-direction:column;gap:24px;width:1100px"><p style="font-family:{SERIF};font-size:200px;line-height:1;font-weight:600;color:#E8EAEE">{big}</p>'
                f'<h2 style="font-family:{SERIF};font-size:48px;line-height:1.3;font-weight:600;color:#E8EAEE">{title}</h2>'
                f'<div style="display:flex;gap:48px;border-top:1px solid #2A3340;padding:20px 0 0"><p style="font-size:22px;line-height:1.6;color:#AEB4BD;width:520px">{left}</p><p style="font-size:22px;line-height:1.6;color:#AEB4BD;width:520px">{right}</p></div></div></div>'
                + footer("资料来源：" + src, strength(stren), n, total, "#8A93A0", "#AEB4BD"))
        return section(sid, body, "#0B0D10", "#E8EAEE", pad="0", extra="") + aside(note)
    add(sid, fn)

# ---------- 发现页 / 建议页 ----------
def findings(sid, chap, lab, title, items, src, note):
    def fn(n, total):
        rows = "".join(f'<div style="display:flex;gap:32px;align-items:start;border-top:1px solid {LINE};padding:16px 0"><p style="font-family:{SERIF};font-size:36px;line-height:1;color:{ACC};width:56px">{i}</p>'
                       f'<div style="flex:1;display:flex;flex-direction:column;gap:4px"><p style="font-size:25px;line-height:1.4;font-weight:700;color:{INK}">{a}</p><p style="font-size:22px;line-height:1.45;color:{GREY}">{b}</p></div>'
                       f'{mono(s, WARM if s != "强" else ACC, 19, "width:100px;text-align:right")}</div>' for i, a, b, s in items)
        body = topbar(chap, lab) + hr() + h2(title) + f'<div style="display:flex;flex-direction:column">{rows}</div>' + footer("证据：" + src, "发现", n, total)
        return section(sid, body) + aside(note)
    add(sid, fn)

def recs(sid, chap, title, items, src, note):
    def fn(n, total):
        rows = "".join(f'<div style="display:flex;gap:32px;align-items:start;border-top:1px solid {LINE};padding:14px 0"><p style="font-family:{SERIF};font-size:36px;line-height:1;color:{ACC};width:56px">{i}</p>'
                       f'<div style="flex:1;display:flex;flex-direction:column;gap:4px"><p style="font-size:24px;line-height:1.4;font-weight:700;color:{INK}">{a}</p><p style="font-size:21px;line-height:1.45;color:{GREY}">依据：{b}</p><p style="font-size:21px;line-height:1.45;color:{WARM}">翻转条件：{c}</p></div>'
                       f'{mono(s, WARM if s != "强" else ACC, 19, "width:100px;text-align:right")}</div>' for i, a, b, c, s in items)
        body = topbar(chap, "建议") + hr() + h2(title, size=44) + f'<div style="display:flex;flex-direction:column">{rows}</div>' + footer(src, "建议", n, total)
        return section(sid, body) + aside(note)
    add(sid, fn)

# ================= 页面内容 =================
divider("d1", "01", "公司与业务边界", [("事实", "2025 年营业总收入 1720.54 亿元、归母净利润 823.20 亿元，酒类占营业收入 99.96%；茅台酒一个产品贡献酒类收入的 86.8%"),
    ("机制", "「单一超高毛利产品 + 并表的集团财务公司」结构：利息收入计入总收入，吸收存款计入负债，总收入、现金流与负债率都带金融噪音"),
    ("判断", "分析茅台必须先把财务公司剥开看，剔除后才是酒的生意；本报告所有现金流与负债结论都按这一口径复核")])
add_stats()
figure("s1-structure", "01 — 公司与业务边界", "图 1-2", "茅台酒占酒类收入 86.8%，直销首次过半，国外不到 3%：一个产品、两条渠道、一个市场", "fig1_2",
       "2025 年主营业务收入按产品、渠道、地区的三组构成", "贵州茅台 2025 年年度报告「主营业务分行业、分产品、分地区、分销售模式情况」[1]；占比由本报告计算", "强",
       "三组口径各自合计 1687.75 亿元。茅台酒毛利率 93.53%、系列酒 76.11%；直销 845.43 亿元、批发代理 842.32 亿元；国外 48.50 亿元、−6.52%。")

divider("d2", "02", "收入与增长拆解", [("事实", "营业总收入 2021–2024 年从 1094.64 亿元增至 1741.44 亿元，2025 年 −1.20%，上市以来首次年度负增长；2026 年前三季 +1.82%"),
    ("机制", "增长曾靠「茅台酒量价齐升 + 系列酒放量 + 直销替代批发」叠加；2025 年系列酒 −9.76%、茅台酒销量仅 +0.73%，只剩直销结构在动"),
    ("判断", "2026 年的恢复来自两次合同价上调而非销量，收入弹性已从「量」切换到「价」，预测必须按价格情景做")])
e3("e3-revenue", "02 — 收入与增长拆解", "e3rev", "−1.2%", "2025 年营业总收入 1720.54 亿元，上市以来首次年度负增长",
   "2021–2024 年年均增长 16.7%，2025 年掉头；2026 年前三季 +1.8%，全部来自两次合同价上调，茅台酒销量数据不支持量增。",
   "归母净利润 −4.53%，降幅大于收入；差额来自销售费用 +28.6% 与利息收入下降。底纹为 2021–2025 年营业总收入走势，纵轴从 0 起。",
   [("1094.64", 990, 326, 160, "left"), ("1741.44", 1440, 134, 150, "center"), ("1720.54", 1600, 216, 170, "left")], [("2021", 1061), ("2023", 1365), ("2025", 1669)],
   "各年年度报告合并利润表 [1][2][3]；2021 年营业总收入为媒体一致转引 [28]", "强", "E3 结论页。底纹用原始数据点重画，无字；数值标签 HTML 叠放。2021 年总收入未开到原文，标中。")
figure("s2-trend", "02 — 收入与增长拆解", "图 2-1", "营业总收入 2021–2024 年年均增长 16.7%，2025 年 −1.2%；2026 年前三季仅 +1.8%，净利润 −0.2%", "fig2_1",
       "2021–2025 年及 2026 年前三季度营业总收入与归母净利润柱状图", "各年年度报告 [1][2][3]、2026 年三季报 [4]；2021 年营业总收入为转引 [28]，2026 年前三季为未审计数", "强",
       "2025 年归母净利润 823.20 亿元（−4.53%）；2026 年前三季营业总收入 1332.84 亿元、归母 644.67 亿元。2026 年柱不与全年相比。")
figure("s2-products", "02 — 收入与增长拆解", "图 2-2", "茅台酒 2025 年收入 +0.4% 停在 1465 亿元，系列酒 −9.8%：第二曲线先于主产品收缩", "fig2_2",
       "2023–2025 年茅台酒与系列酒收入柱状图", "年报「主营业务分产品情况」与「产品情况」表 [1][2][3]", "强",
       "吨价（销售收入 ÷ 销量）：茅台酒 300.6 → 314.4 → 313.4 万元/吨；系列酒 66.2 → 66.9 → 58.1 万元/吨。系列酒销量 +3.88% 而收入 −9.76%，年报解释为产品结构调整，即降档走量。")
figure("s2-channels", "02 — 收入与增长拆解", "图 2-3", "直销占比 2026 年前三季升到 56.4%；i 茅台 2026 年口径跳到 585.62 亿元，不能与往年连成一条线", "fig2_3",
       "直销占比折线与 i 茅台收入柱状图", "年报「分销售模式」「线上销售情况」[1][2][3]，季报「销售情况」及注 [4][5]；2026 年半年报将直销定义改为含代售 [6]", "中",
       "2026 年半年报把直销定义改为「线下自营门店、i 茅台平台、代售等」，新增「自售 + 经销 + 代售」模式；i 茅台 2026 年数字含经平台结算的经销商销售，与 2023–2025 年平台自营零售口径不可比。批发代理 2025 年 −12.1%。")

divider("d3", "03", "盈利与成本结构", [("事实", "2025 年酒类毛利率 91.23%，仅比 2024 年降 0.78 个百分点；销售费用率从 2022 年 2.66% 升到 4.30%，税金及附加率从 14.90% 升到 16.20%"),
    ("机制", "毛利率由产品结构锁定（茅台酒 93.5%、系列酒 76.1%），利润的边际变化来自费用与税：销售费用 2025 年 +28.6%"),
    ("判断", "盈利风险不在成本端，而在「稳价格要花多少钱」：2025 年多花的 16.1 亿元销售费用是为直销渠道与市场秩序付的账")])
figure("s3-margin", "03 — 盈利与成本结构", "图 3-1", "酒类毛利率三年只降 0.88 个百分点到 91.23%，系列酒拖累 3.76 个百分点", "fig3_1",
       "2023–2025 年茅台酒、酒类合计、系列酒毛利率折线", "年报「主营业务分产品情况」[1][2][3]，毛利率为年报原值", "强",
       "2025 年营业成本 148.92 亿元（+8.0%），茅台酒成本 +9.50% 而销量 +0.73%，年报解释为生产成本上涨。")
figure("s3-expense", "03 — 盈利与成本结构", "图 3-2", "销售费用率 2022 年 2.66% 升到 2025 年 4.30%，税金及附加率升到 16.20%：利润变化在费用不在毛利", "fig3_2",
       "2022–2025 年税金及附加、管理费用、销售费用占营业收入比例折线", "各年合并利润表 [1][2][3]；比例 = 该项 / 营业收入（不含利息收入），本报告计算", "强",
       "2025 年销售费用 72.53 亿元、比 2024 年多 16.14 亿元；管理费用连续三年下降（93.16 → 83.20 亿元）。2026 年前三季销售费用 48.31 亿元、+7.9%。加权 ROE 36.02% → 32.53%。")

divider("d4", "04", "现金流与资产负债", [("事实", "2025 年经营活动现金流 615.22 亿元（−33.5%），但销售商品收到的现金 1839.90 亿元仍比 2024 年多；合同负债从 2022 年末 154.72 亿元降到 2026 年 9 月末 20.84 亿元"),
    ("机制", "经营现金流的波动一半来自财务公司存款进出，另一半来自渠道预收款消失：经销商不再提前打款，公司对下游的占款能力在缩减"),
    ("判断", "茅台不缺现金，缺的是现金流前瞻指标：合同负债的连续下降比收入负增长更早、更准确地预告了需求转弱")])
figure("s4-cashflow", "04 — 现金流与资产负债", "图 4-1", "2025 年经营现金流 −33.5% 中一半是财务公司存款进出，剔除后真实回款约 −18%", "fig4_1",
       "2022–2025 年经营现金流分解为剔除存款后的现金流与存款净增加额", "各年合并现金流量表 [1][2][3]；「存款净增加额」即客户存款和同业存放款项净增加额", "强",
       "剔除财务公司后的经营现金流：2023 年 674.0、2024 年 814.0、2025 年 666.2 亿元。经营现金流 / 归母净利润：0.59、0.89、1.07、0.75，低于 1 的年份都对应存款流出。筹资活动每年净流出 570–710 亿元，几乎全是分红与回购。")
e3("e3-contract", "04 — 现金流与资产负债", "e3con", "20.84 亿", "合同负债从 2022 年末 154.72 亿元降到 2026 年 9 月末 20.84 亿元，只剩半个月批发收入",
   "合同负债是经销商预付货款，它比收入早一年转向：2023 年收入 +18% 时合同负债已 −8.7%，2024 年收入 +15.7% 时它 −32%。",
   "2026 年「代售、按佣金结算」模式下经销商不再预付，渠道蓄水池放空；应收款项融资从零到 44.57 亿元，公司开始接受承兑汇票回款。",
   [("154.72", 1075, 150, 150, "left"), ("20.84", 1540, 436, 150, "right")], [("2022-12", 1053), ("2024-12", 1407), ("2026-09", 1716)],
   "各年合并资产负债表 [1][2][3]、季报 [4][5][6]；2026 年为未审计数", "中", "E3 结论页，底纹为七个时点的合同负债期末余额。")
figure("s4-contract", "04 — 现金流与资产负债", "图 4-2", "合同负债七个时点连降，2026 年 6 月起低于一个月批发收入（约 70 亿元）", "fig4_2",
       "2022 年末至 2026 年 9 月末合同负债期末余额柱状图", "各年合并资产负债表 [1][2][3]、2025 年三季报 [5]、2026 年半年报 [6] 与三季报 [4]；一个月批发收入按 2025 年批发代理收入 ÷ 12 估算", "中",
       "2025-09 77.49、2025-12 80.07、2026-06 31.78、2026-09 20.84 亿元。2026 年按前三季批发收入 571.20 ÷ 9 ≈ 63 亿元/月。")
table_page("s4-balance", "04 — 现金流与资产负债", "表 4-3", "货币资金降到 516.91 亿元、存货升到 614.27 亿元，货币资金的 56% 存放在集团财务公司",
           ["年末", "货币资金", "存货", "吸收存款及同业存放", "负债合计 / 负债率", "标签 · 强度"],
           [["2022", "582.74", "388.24", "128.74", "495.63 / 19.5%", "实际值 · 强"], ["2023", "690.70", "464.35", "120.34", "490.43 / 18.0%", "实际值 · 强"],
            ["2024", "592.96", "543.43", "231.03", "569.33 / 19.0%", "实际值 · 强"], ["2025", "516.91", "614.27", "180.38", "498.76 / 16.4%", "实际值 · 强"],
            ["2026-09", "499.27", "—", "172.72", "378.83 / 11.9%", "实际值 · 中（未审计）"]],
           "各年合并资产负债表 [1][2][3][4]（亿元）；财务公司风险评估报告 [8]：2026 年 6 月末公司在财务公司存款 301.45 亿元，占同期货币资金 535.19 亿元的 56%", "强",
           "存货几乎全是基酒：2025 年末半成品酒 315,207.51 吨、成品酒 24,770.35 吨；茅台酒从生产到出厂至少五年，存货增长是产能释放的结果。财务公司资本充足率 20.94%、不良率 0，但年报注明不可随时支取的同业存款增加。应收款项融资 44.57 亿元在 2025 年末首次出现。",
           widths=[12, 15, 13, 22, 20, 18])

divider("d5", "05", "同业对比", [("事实", "2025 年四家里茅台营业收入 −1.2%、汾酒 +7.5%、泸州老窖 −17.5%、五粮液 −54.6%（重述）；2026 年前三季泸州老窖 −36.6%、汾酒 −13.8%，茅台 +2.0% 是唯一没有两位数下滑的"),
    ("机制", "行业需求收缩（2025 年规上白酒产量 −12.1%）先打到依赖经销商压货的公司：五粮液把 2025 年前三季收入调减 303 亿元改按终端确认，泸州老窖经营现金流 −62.9%"),
    ("判断", "茅台的相对优势在 2026 年被放大；同业的调整方式说明行业正在把渠道库存转回报表，茅台合同负债归零是同一过程的温和版本")])
table_page("s5-table1", "05 — 同业对比", "表 5-2a", "2025 年茅台毛利率 91.2%、销售费用率 4.3%：同业毛利率低 4–16 个百分点、销售费用率高 6–14 个百分点",
           ["指标（2025 年，亿元 / %）", "贵州茅台", "五粮液（重述）", "泸州老窖", "山西汾酒"],
           [["营业收入 / 同比", "1688.38 / −1.2", "405.29 / −54.6", "257.31 / −17.5", "387.18 / +7.5"], ["归母净利润 / 同比", "823.20 / −4.5", "89.54 / −71.9", "108.31 / −19.6", "122.46 / +0.0"],
            ["毛利率（1 − 成本 / 收入）", "91.2", "77.5", "86.6", "74.9"], ["销售费用率", "4.3", "18.8", "12.6", "10.6"], ["税金及附加率", "16.2", "27.2", "15.3", "17.9"], ["经营活动现金流净额", "615.22", "297.06", "71.23", "90.14"]],
           "四家 2025 年年度报告原文 [1][24][25][26]；比率为本报告按三表计算（实际值 · 强）。五粮液为重述后口径，与其 2024 年不可比", "强",
           "泸州老窖毛利率 86.6% 最接近茅台，但销售费用率是茅台的三倍。五粮液税金及附加率 27.2% 与其收入基数被调减、消费税按发货缴纳有关。", widths=[28, 18, 18, 18, 18])
table_page("s5-table2", "05 — 同业对比", "表 5-2b", "茅台合同负债 / 收入 4.7% 已是四家最低；五粮液 223% 的分红率是重述把分母压小",
           ["指标（2025 年）", "贵州茅台", "五粮液（重述）", "泸州老窖", "山西汾酒"],
           [["合同负债（年末，亿元）", "80.07", "134.60", "33.67", "70.07"], ["合同负债 / 营业收入", "4.7%", "33.2%", "13.1%", "18.1%"], ["加权 ROE", "32.5%", "6.9%", "22.7%", "33.5%"],
            ["现金分红 / 归母净利润", "79.0%", "223.5%", "78.5%", "65.4%"], ["审计意见", "天健 · 标准无保留", "天职国际 · 标准无保留", "信永中和 · 标准无保留", "天衡 · 标准无保留"]],
           "四家 2025 年年度报告原文 [1][24][25][26]；五粮液另有「其他流动负债」270.29 亿元为重述后单列的已收款未确认收入", "强",
           "茅台预收款比例最低，与其代售、按佣金结算的渠道模式一致。茅台分红率不含回购；含回购 61.20 亿元为 86.4%。", widths=[28, 18, 18, 18, 18])
figure("s5-growth", "05 — 同业对比", "图 5-2", "2026 年前三季泸州老窖 −36.6%、汾酒 −13.8%，茅台 +2.0% 是四家里唯一没有两位数下滑的", "fig5_2",
       "四家公司 2025 年与 2026 年前三季营业收入同比条形图", "四家 2025 年年度报告与 2026 年第三季度报告 [1][4][24][25][26]；五粮液 2026 年同比以重述后基数计算，不代表真实恢复", "中",
       "2026 年前三季：茅台 1309.71 亿元 +2.0%，五粮液 328.58 亿元 +7.3%（重述基数），泸州老窖 146.68 亿元 −36.6%，汾酒 283.82 亿元 −13.8%。五粮液经营现金流 0.47 亿元（−99.8%）。行业：2025 年规上白酒产量 354.9 万千升、−12.1%，连续九年下降 [12]。")
table_page("s5-wly", "05 — 同业对比", "表 5-3", "五粮液把 2025 年前三季收入从 609.45 亿元调减到 306.38 亿元：行业收入确认口径在收紧",
           ["期间", "营业收入 更正前 → 后（亿元）", "归母净利润 更正前 → 后", "资产负债表对应"],
           [["2025 Q1", "369.40 → 170.86（−198.55）", "148.60 → 44.16", "其他流动负债 +185.89 亿元"], ["2025 H1", "527.71 → 235.10（−292.61）", "194.92 → 46.24", "其他流动负债 +273.26 亿元"],
            ["2025 Q1–Q3", "609.45 → 306.38（−303.08，−49.7%）", "215.11 → 64.75", "其他流动负债 +274.42 亿元；不影响现金流量表"], ["公告理由（原文）", "「对 2025 年业务模式进行梳理，基于谨慎性原则，调整 2025 年部分业务收入确认相关核算」", "—", "未说明具体业务"]],
           "五粮液《关于前期会计差错更正的公告》（2026/第 011 号，2026-04-30）[24]（实际值 · 强）；调整性质的解读为推断 · 中", "强",
           "调整方向与「已发货但未满足确认条件的货款转入负债」一致。茅台 2026 年代售模式的会计效果相同，只是用业务模式变化实现。两家合同负债在 2026 年 9 月末都在下降：茅台 20.84、五粮液 89.27 亿元。", fs=24, widths=[14, 34, 22, 30])

divider("d6", "06", "预算与预测（模型输出）", [("事实", "管理层目标 2023、2024 年均完成（15%，实际 +18.0%、+15.7%），2025 年目标 9% 实际 −1.2%，2026 年年报首次没有写数字目标；合同价两次上调累计 +17.1%，前三季茅台酒收入只 +2.2%"),
    ("机制", "价格上调由「合同价 → 批价」价差决定能否传导：批价 1650 元上下、合同价 1369 元，经销商毛利已压到两成，提价空间转为渠道利润而非公司收入"),
    ("判断", "按前三季实际传导率外推，FY2026 营业总收入 1736–1780 亿元（+0.9% 至 +3.5%），低于两家券商 4 月的预测；本章强度「中」，受最弱输入限制")])
table_page("s6-targets", "06 — 预算与预测", "表 6-1", "目标 15% → 15% → 9% → 不给数字：2025 年目标首次未完成，2026 年年报经营计划没有数字目标",
           ["年度", "目标（年报经营计划）", "实际", "完成", "标签 · 强度"],
           [["2023", "营业总收入 +15% 左右", "+18.04%", "是", "厂商自述 · 中 [29]；实际值 · 强"], ["2024", "+15% 左右；固定资产投资 61.79 亿元", "+15.66%", "是", "厂商自述 · 强 [3]；实际值 · 强"],
            ["2025", "+9% 左右；固定资产投资 47.11 亿元", "−1.20%", "否", "厂商自述 · 强 [2]；实际值 · 强"], ["2026", "未写数字目标，仅列八方面工作", "前三季 +1.82%", "—", "厂商自述 · 强 [1]；实际值 · 中"]],
           "2023、2024、2025 年年度报告「经营计划」[1][2][3]；2023 年目标为 2022 年年报经媒体转引 [29]；2025-05 股东大会表述 [23]", "强",
           "2025 年目标从 15% 降到 9% 时，董事长在股东大会称是权衡自身与环境后定下的可行目标，最终未完成。2026 年不再给数字，可读作管理层对需求能见度的判断。", widths=[10, 34, 16, 10, 30], warm_rows=(2,))
figure("s6-prices", "06 — 预算与预测", "图 6-2", "合同价三年两级跳到 1369 元，散瓶批价从 2220 元跌到 1650 元：经销商价差从 47% 压到 17%", "fig6_2",
       "2023–2026 年飞天合同价阶梯与散瓶批价折线", "公司重大事项公告 [7]；2023-11 与 2026-03 调价为公告经媒体转引 [15][30]；批价为今日酒价经财联社、界面、第一财经转引 [14]，不是公司披露数据", "中",
       "2025 年初价差 2220 − 1169 = 1051 元（约 47%）；2026 年 7 月 1655 − 1369 = 286 元（约 17%）。2025-12 批价 1485 元跌破 1499 元零售价。2026-07-18 公告：合同价 1269 → 1369，i 茅台零售价 1539 → 1639。")
figure("s6-scenarios", "06 — 预算与预测", "图 6-3", "FY2026 营业总收入情景 1736 / 1754 / 1780 亿元（+0.9% / +1.9% / +3.5%），低于两家券商 4 月的预测", "fig6_3",
       "FY2026 营业总收入三情景柱状图与券商预测参考线", "模型输出。输入：茅台酒与系列酒 2025 年收入 [1]（强）、2026 年前三季分产品增速 [4][5]（中）、利息收入持平假设 [1]；乐观 / 悲观档 g₁ 为推断（弱）；对照 [19]", "中",
       "模型：FY2026 营业总收入 = 茅台酒 2025 收入 ×(1+g₁) + 系列酒 2025 收入 ×(1+g₂) + 利息收入与其他 32.80 亿元。g₂ = +0.47%。g₁ 基准 +2.18%（前三季实际）、乐观 +4.0%、悲观 +1.0%。归母按净利率 47.9% 持平约 832 / 840 / 853 亿元；2026 年前三季归母 −0.25% 说明净利率持平偏乐观。华泰 2026E 1807.43、国信 1776.12 亿元（各一家，预测 · 弱）。")

divider("d7", "07", "风险预警", [("事实", "八项预警指标中五项触发：合同负债 20.84 亿元、批价与合同价价差 17%、系列酒收入 −9.8%、销售费用率 4.30%、国外收入 −57.8%；审计意见连续五年标准无保留，负债率 11.9%"),
    ("机制", "风险集中在需求与渠道一端：2025 年 5 月修订的公务接待规定压缩政商务消费，批价下行到零售价以下，经销商预付消失；公司用提价与直销对冲，又把利润从渠道端抽回"),
    ("判断", "财务风险低、经营风险中、治理风险中偏高：五年四任董事长、两任被查，2026 年首次不给数字目标，是管理连续性的硬信号")])
table_page("s7-matrix1", "07 — 风险预警", "表 7-1a", "八项预警指标中五项触发：合同负债、价差、系列酒、费用率、国外收入",
           ["指标", "阈值（本报告设定）", "当前值", "状态", "标签 · 强度"],
           [["合同负债 / 月均批发收入", "< 1 个月", "20.84 / 约 63 = 0.3 个月", "触发", "实际值（计算）· 中 [4]"], ["散瓶批价 − 合同价", "价差 < 25%", "(1655 − 1369) / 1655 = 17%", "触发", "估计 · 中 [7][15]"],
            ["系列酒收入增速", "连续两期为负", "2025 年 −9.8%；2026 前三季 +0.5%", "触发（2025），2026 解除", "实际值 · 强 / 中 [1][4]"], ["销售费用率", "> 4%", "2025 年 4.30%；2026 前三季 3.69%", "触发（2025）", "实际值（计算）· 强 / 中"],
            ["国外收入增速", "< −20%", "2026 前三季 −57.8%", "触发", "实际值 · 中 [4][5]"]],
           "年报与季报 [1][4][5]、调价公告 [7]、媒体转引的批价 [14][15]。阈值为本报告设定，不是行业标准；月均批发收入 2026 年按 571.20 ÷ 9 ≈ 63 亿元", "中",
           "需求传导路径：公务消费（2025-05-18 条例修订）→ 批价 → 经销商进货意愿 → 预收款。2025 年批发代理收入 −12.1%、合同负债 −16.5%。", widths=[22, 16, 28, 16, 18], warm_rows=(0, 1, 2, 3, 4))
table_page("s7-matrix2", "07 — 风险预警", "表 7-1b", "三项未触发：剔除财务公司后的现金流 / 净利 0.81 临界，审计意见连续五年标准无保留，负债率 11.9%",
           ["指标", "阈值（本报告设定）", "当前值", "状态", "标签 · 强度"],
           [["剔除财务公司的经营现金流 / 归母净利", "< 0.8", "2025 年 666.2 / 823.2 = 0.81", "正常（临界）", "实际值（计算）· 强 [1]"], ["审计意见", "非标准意见", "2021–2025 均标准无保留（天职国际 → 天健）", "正常", "实际值 · 强 [1][2][3]"],
            ["资产负债率（含吸收存款）", "> 30%", "2026-09 11.9%", "正常", "实际值（计算）· 中 [4]"]],
           "年报 [1][2][3]、2026 年三季报 [4]。审计机构 2024 年由天职国际（服务 6 年）改聘天健，早于天职国际 2024-08 被证监会处罚四个月 [17]，属合规动作", "强",
           "消费税：现行白酒在生产环节 20% + 0.5 元/500 克，后移征收环节尚无时间表 [21]；2025 年税金及附加 273.54 亿元、占营业收入 16.2%。市值：2021-02 高点 2627.88 元/股、超 3 万亿元；2025-10-30 收盘 1431.90 元、约 1.79 万亿元 [20]。", widths=[26, 14, 30, 14, 16])
table_page("s7-governance", "07 — 风险预警", "表 7-4", "五年四任董事长、两任被查；2026 年年报首次不给数字目标与投资额：任期短于一个基酒生产周期",
           ["时间", "事项", "后续", "标签 · 强度"],
           [["2020-03", "高卫东接任董事长", "2022-05 被查，2024-02 一审无期", "实际值 · 中 [18]"], ["2021-08", "丁雄军接任", "2024-04 卸任，后被调查（日期未核）", "实际值 · 中 [18]"],
            ["2024-04", "张德芹接任", "2025-10-27 辞职（工作调整）", "实际值 · 中 [18]"], ["2025-10", "陈华获推荐为董事长人选", "总经理由王莉代行（2023-08 起）", "实际值 · 中 [18][23]"],
            ["2024-04", "审计机构由天职国际改聘天健", "2024-08 天职国际因他案被暂停证券业务 6 个月", "实际值 · 强 [2][17]"], ["2026-04", "2025 年报经营计划无数字目标、无固定资产投资额", "前三年均有", "实际值 · 强 [1][2][3]"]],
           "年报 [1][2][3]、公司公告经媒体转引 [17][18]、业绩说明会报道 [23]", "中",
           "茅台酒从生产到出厂至少五年；五年四任董事长意味着技改（155 亿元）、国际化等长期投资的决策连续性缺乏保障。2025-11-06 业绩说明会上代总经理王莉称行业正经历深度调整。", widths=[12, 34, 34, 20])

divider("d8", "08", "发现与建议", [("事实", "八条发现里六条强度为「强」（三表原文），两条为「中」（治理事件与批价来自转引）"),
    ("机制", "需求收缩 → 批价下行 → 经销商预付消失 → 公司用提价与直销对冲 → 费用上升、价差压缩 → 增长只剩价格一项"),
    ("判断", "四条建议指向同一件事：把管理指标从「营收增速」换成「渠道健康度」；每条建议写明依据与翻转条件")])
findings("findings1", "08 — 发现与建议", "发现 1–4", "增长停摆、渠道换挡、定价空间用尽、系列酒先收缩",
         [("1", "增长停摆：2025 年营业总收入 −1.2%，上市以来首次年度负增长；2026 年前三季 +1.8% 全部来自两次合同价上调", "年报与季报原文 [1][4]；茅台酒销量数据不支持量增（第二章、第六章）", "强"),
          ("2", "渠道换挡：直销占比 45.7% → 56.4%，合同负债 154.72 亿元 → 20.84 亿元，应收款项融资从零到 44.57 亿元", "各年资产负债表与季报 [1][3][4]（第二章、第四章）", "强"),
          ("3", "定价空间用尽：合同价 1169 → 1369 元（+17.1%）只换来前三季茅台酒收入 +2.2%，经销商价差从约 47% 压到约 17%", "公告 [7] 与转引的批价 [14][15]（第六章）", "中"),
          ("4", "系列酒先于主产品收缩：2025 年收入 −9.8%、吨价 −13%，降档走量；2026 年前三季仅 +0.5%", "年报与季报 [1][4]（第二章）", "强")],
         "[1][3][4][7][14][15]", "发现页一。强度：三表原文为强；批价与价差为中。")
findings("findings2", "08 — 发现与建议", "发现 5–8", "利润变化在费用、现金流一半是口径噪音、同业优势放大、治理连续性弱",
         [("5", "利润质量变化在费用不在毛利：毛利率三年只降 0.9 个百分点，销售费用率 2.66% → 4.30%，税金及附加率 14.9% → 16.2%", "各年利润表 [1][2][3]（第三章）", "强"),
          ("6", "现金流有一半是口径噪音：2025 年经营现金流 −33.5% 中 161.59 亿元来自财务公司存款；剔除后 −18%；56% 的货币资金在财务公司", "现金流量表 [1][2] 与财务公司风险评估报告 [8]（第一章、第四章）", "强"),
          ("7", "同业对照下优势放大：四家里唯一 2026 年未两位数下滑；毛利率高 4–16 个百分点、销售费用率低 6–14 个百分点；但合同负债 / 收入 4.7% 已是最低", "四家年报原文 [1][24][25][26]（第五章）", "强"),
          ("8", "治理连续性弱于生产周期：五年四任董事长、两任被查；2026 年报首次不给数字目标；分红 + 回购 86% 仍未止住净资产增长，ROE 36.0% → 32.5%", "年报 [1][2][3] 与治理事件转引 [18]（第三章、第七章）", "中")],
         "[1][2][3][8][18][24][25][26]", "发现页二。第 6 条存款占比为中，其余三表数字为强。")
recs("recs", "08 — 发现与建议", "把管理指标从营收增速换成渠道健康度：四条建议，各带依据与翻转条件",
     [("1", "把「合同负债 / 月均批发收入」与「批价 − 合同价价差」设为董事会层面的前瞻 KPI，替代年度营收增速目标", "发现 2、3、8；2026 年年报已不给数字目标，正是切换时机", "合同负债回到 70 亿元以上（一个月批发收入）且价差连续两季高于 25%", "中"),
      ("2", "批价低于 1700 元期间不再上调合同价，价格工具换成投放量与产品结构控制；提价留到价差回到 30% 以上", "发现 1、3", "散瓶批价站上 1900 元且经销商价差高于 30%，提价对收入的传导率会回到 2023 年水平", "中"),
      ("3", "定期报告增加「剔除财务公司」的经营现金流与负债率口径，并把在财务公司的存款占货币资金比例设上限（建议 50%）", "发现 6", "财务公司不再并表，或年报披露同业存款全部可随时支取", "强"),
      ("4", "在 ROE 回到 35% 之前，把现金分红比率提到 90% 以上或把回购常态化（每年 60 亿元量级）", "发现 7、8", "技改（155 亿元）或国际化出现回报率高于当期 ROE 的投资项目，留存收益应优先投入", "强")],
     "依据编号对应发现页；强度取依据中最弱一条；翻转条件为出现该证据时本条建议作废。阈值为本报告设定，需公司内部渠道库存与动销数据校准（未公开）",
     "建议页。本报告不做 STP/4P，不对经销商或投资者提建议。")

# ================= 输出 =================
order = [sid for sid, _ in PAGES]; total = len(order)
for i, (sid, fn) in enumerate(PAGES, 1):
    open(os.path.join(OUT, "slides", sid + ".html"), "w", encoding="utf-8").write(_fix_aside(fn(i, total)))
sections = {"intro": {"description": "封面与方法", "start": "cover"}}
names = {"d1": "第一章 公司与业务边界", "d2": "第二章 收入与增长拆解", "d3": "第三章 盈利与成本结构", "d4": "第四章 现金流与资产负债", "d5": "第五章 同业对比", "d6": "第六章 预算与预测", "d7": "第七章 风险预警", "d8": "第八章 发现与建议"}
for k, v in names.items(): sections[k] = {"description": v, "start": k}
deck = {"v": 4, "createdOnFiles": {"v": 1, "at": "2026-11-05T08:00:00Z"}, "lists": "css", "title": "贵州茅台经营分析 2026", "order": order, "sections": sections,
        "faces": {"noto-serif-sc": {"family": "Noto Serif SC", "href": "https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600&display=swap"},
                  "noto-sans-sc": {"family": "Noto Sans SC", "href": "https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap"},
                  "ibm-plex-mono": {"family": "IBM Plex Mono", "href": "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap"}}, "designSystems": []}
json.dump(deck, open(os.path.join(OUT, "deck.json"), "w", encoding="utf-8"), ensure_ascii=False)
print(total, "slides:", " ".join(order))
