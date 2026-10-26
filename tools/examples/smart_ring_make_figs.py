"""范例：智能戒指行业调研（2026-10）的幻灯片版图表，演示 deckfig 的用法。数据来自检索摘要，复用前须重新取证。
运行：python3 tools/examples/smart_ring_make_figs.py（图写到当前目录 figs_deck/）"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import datetime as dt
import matplotlib.dates as mdates
import deckfig as D
from deckfig import plt, np, box, arrow, tidy, wrap_cjk, C, TXT, TXT2, MUTED, LIGHT, BLUE, WARM

GREY = "#B9B4A8"; GREEN = C[2]; GOLD = C[3]
d = dt.date.fromisoformat

# ---------- fig1 boundary ----------
fig, ax = D.blank(9.1, 3.7)
ax.text(0.5, 0.965, "计入本报告规模：健康传感戒指", ha="center", fontsize=13, weight="bold", color=BLUE)
cats = [("健康订阅型", "Oura Ring 4 / 5\n349–499 美元\n+ 会员 5.99 美元/月"),
        ("手机生态型", "Galaxy Ring\n399 美元，无订阅\n部分功能需三星手机"),
        ("平价无订阅型", "RingConn、Amazfit\nUltrahuman\n199–479 美元"),
        ("医疗 / 临床型", "EvieMED 获 510(k)\nCircular 2 带 ECG\n面向 B2B 与临床")]
for i, (h, t) in enumerate(cats):
    x = 0.03 + i * 0.2425
    box(ax, x, 0.50, 0.225, 0.40, "", fc="#FFFFFF", ec=BLUE, lw=1.4)
    ax.text(x + 0.1125, 0.84, h, ha="center", va="center", fontsize=12.5, weight="bold", color=BLUE)
    ax.text(x + 0.1125, 0.665, t, ha="center", va="center", fontsize=11, color=TXT, linespacing=1.4)
ax.plot([0.03, 0.97], [0.43, 0.43], color=MUTED, lw=0.8, ls=(0, (4, 3)))
ax.text(0.5, 0.36, "不计入规模，只作替代品与配套分析", ha="center", fontsize=12.5, weight="bold", color=TXT2)
adj = [("NFC / 支付戒指", "无生物传感器\n计入后出货量约 ×25"),
       ("智能手表", "2025 年 1.635 亿块\n戒指约为其 2.6%"),
       ("手环 / 无屏手带", "WHOOP、Garmin\n同样主打睡眠恢复"),
       ("上游与配套", "芯片、曲面电池\nApp 与第三方数据")]
for i, (h, t) in enumerate(adj):
    x = 0.03 + i * 0.2425
    box(ax, x, 0.02, 0.225, 0.29, "", fc=LIGHT, ec=GREY, lw=1.0)
    ax.text(x + 0.1125, 0.245, h, ha="center", va="center", fontsize=12, weight="bold", color=TXT2)
    ax.text(x + 0.1125, 0.115, t, ha="center", va="center", fontsize=10.5, color=TXT2, linespacing=1.35)
D.save(fig, "fig1_boundary.png")

# ---------- fig2 timeline (等距排列，日期标注) ----------
fig, ax = plt.subplots(figsize=(9.1, 3.4))
ev = [("2015-08", "Oura\nKickstarter"), ("2021-10", "Oura Gen3\n会员制起步"), ("2024-01", "Amazfit Helio\nCES 发布"),
      ("2024-07", "Galaxy Ring\n399 美元"), ("2024-10", "Oura Ring 4"), ("2024-12", "Oura D 轮\n估值 52 亿美元"),
      ("2025-08", "ITC 终裁\nOura 胜诉"), ("2025-10", "排除令生效\nE 轮估值 110 亿"), ("2026-03", "Ultrahuman\n改款回归美国"),
      ("2026-05", "Oura Ring 5"), ("2026-09", "Oura 递交 S-1\nIPO 推迟")]
ax.axhline(0, color=TXT2, lw=1.2, zorder=1)
for i, (ds, txt) in enumerate(ev):
    s = 1 if i % 2 == 0 else -1
    c = WARM if ("ITC" in txt or "排除令" in txt or "IPO" in txt) else BLUE
    ax.plot([i, i], [0, 0.42 * s], color=GREY, lw=0.9, zorder=1)
    ax.plot(i, 0, "o", color=c, ms=8, zorder=2)
    ax.text(i, 0.47 * s, ds, ha="center", va="bottom" if s > 0 else "top", fontsize=11, weight="bold", color=c)
    ax.text(i, 0.47 * s + 0.2 * s, txt, ha="center", va="bottom" if s > 0 else "top", fontsize=10.5, color=TXT, linespacing=1.25)
ax.text(0.5, -0.12, "≈6 年仅 Oura 一家", ha="center", va="top", fontsize=10, color=MUTED)
ax.set_ylim(-1.25, 1.25); ax.set_xlim(-0.6, len(ev) - 0.4); ax.axis("off")
D.save(fig, "fig2_timeline.png")

# ---------- fig2 estimates vs bottom-up ----------
fig, ax = plt.subplots(figsize=(9.1, 3.5))
est = [("Ken Research", 14.20), ("GMI（新版）", 6.976), ("R&M / GIA", 4.901), ("Grand View", 4.175),
       ("Fortune BI", 4.169), ("Mordor", 4.10), ("R&M（另一报告）", 3.712), ("QYResearch", 3.24), ("GMI（旧版）", 3.106)]
y = np.arange(len(est))[::-1]
ax.barh(y, [v for _, v in est], color=GREY, height=0.62)
for yi, (n, v) in zip(y, est):
    ax.text(v + 0.15, yi, f"{v:.1f}", va="center", fontsize=10.5, color=TXT2)
ax.set_yticks(y); ax.set_yticklabels([n for n, _ in est], fontsize=10.5)
ax.axvline(9.079, color=BLUE, lw=2)
ax.text(9.3, 4.6, "Oura 一家 FY2025 收入\n9.08 亿美元（S-1）", color=BLUE, fontsize=11, weight="bold", va="center")
ax.axvspan(13, 18, color=WARM, alpha=0.12, lw=0)
ax.text(15.5, 1.2, "自下而上推断\n全球约 13–18 亿\n（出货 × 均价 + 订阅）", color=WARM, fontsize=10.5, ha="center", va="center")
ax.set_xlim(0, 19); ax.set_xlabel("2025 年全球智能戒指市场规模（亿美元）")
tidy(ax, ygrid=False); ax.xaxis.grid(True); ax.set_axisbelow(True)
D.save(fig, "fig2_estimates.png")

# ---------- fig2 shipments ----------
fig, ax = plt.subplots(figsize=(9.1, 3.4))
yrs = ["2023", "2024", "2025", "2026E", "2030E"]
src = {"IDC": [0.88, None, 4.3, 4.9, 6.3], "Omdia": [0.85, 1.8, 4.0, 6.0, None],
       "Futuresource": [None, None, 4.1, None, None], "CCS Insight": [None, None, None, 6.0, 15.0]}
cols = {"IDC": BLUE, "Omdia": GREEN, "Futuresource": GOLD, "CCS Insight": WARM}
w = 0.19; x = np.arange(len(yrs))
for i, (k, vals) in enumerate(src.items()):
    for j, v in enumerate(vals):
        if v is None: continue
        ax.bar(x[j] + (i - 1.5) * w, v, w * 0.92, color=cols[k], label=k if j == next(jj for jj, vv in enumerate(vals) if vv is not None) else None)
        ax.text(x[j] + (i - 1.5) * w, v + 0.25, f"{v:g}", ha="center", fontsize=10, color=TXT2)
ax.set_xticks(x); ax.set_xticklabels(yrs); ax.set_ylabel("全球出货（百万枚）"); ax.set_ylim(0, 16.5)
ax.annotate("2025 年三家一致：\n410–430 万枚", xy=(1.75, 5.2), xytext=(1.0, 10.5), fontsize=11, color=TXT, ha="center", va="bottom",
            arrowprops=dict(arrowstyle="-", color=GREY, lw=0.9))
ax.annotate("2026 年分歧：\nIDC +12.8% vs CCS +53%", xy=(3.0, 7.0), xytext=(3.2, 11.5), fontsize=11, color=WARM, ha="center", va="bottom",
            arrowprops=dict(arrowstyle="-", color=GREY, lw=0.9))
tidy(ax); ax.legend(frameon=False, ncol=4, loc="upper left")
D.save(fig, "fig2_shipments.png")

# ---------- fig3 PEST ----------
fig, ax = D.blank(9.1, 3.8)
quad = [("政策 P", "中性偏利好", BLUE, ["FDA 2026-01 放宽一般健康指南", "三星戒指呼吸暂停功能获 510(k)", "ITC 排除令成为准入门槛", "对华关税 2025-04 一度达 145%"]),
        ("经济 E", "订阅支撑利润", GREEN, ["Oura 每枚收入 332→311 美元", "会员收入占比 16%→20%", "Oura 估值 110 亿，IPO 推迟", "印度 2025 年出货 −30.6%"]),
        ("社会 S", "早期采用者为主", GOLD, ["美国成年人 8% 拥有，手表 43%", "Oura 付费会员 72% 为女性", "HHS 力推全民可穿戴", "消费级数据不受 HIPAA 保护"]),
        ("技术 T", "小型化与电池瓶颈", WARM, ["Ring 5 厚 2.28 mm、重 2–2.7 g", "电池仅 10–24 mAh，续航 4–15 天", "心率/HRV 一致性 0.97–0.99", "四期睡眠 53%–79%，有争议"])]
for i, (h, tag, c, items) in enumerate(quad):
    x = 0.01 + (i % 2) * 0.5; y = 0.52 - (i // 2) * 0.5
    box(ax, x, y, 0.475, 0.455, "", fc="#FFFFFF", ec=c, lw=1.5)
    ax.text(x + 0.02, y + 0.39, h, fontsize=13.5, weight="bold", color=c, va="center")
    ax.text(x + 0.455, y + 0.39, tag, fontsize=11.5, color=c, va="center", ha="right")
    for j, it in enumerate(items):
        ax.text(x + 0.025, y + 0.30 - j * 0.078, "· " + it, fontsize=11, color=TXT, va="center")
D.save(fig, "fig3_pest.png")

# ---------- fig4 chain ----------
fig, ax = D.blank(9.1, 3.7)
layers = [("上游：芯片与传感", BLUE, ["主控：Ambiq（Oura 5）、Infineon（Oura 4）、Nordic（Galaxy Ring）", "光学前端 ADI；电源管理 ADI、TI；NFC NXP；存储 兆易创新"]),
          ("上游：电池与结构", BLUE, ["曲面锂聚合物电芯 6–24 mAh（Grepow 等定制）", "钛外壳约占非电子 BOM 29%；另有氧化锆陶瓷款"]),
          ("中游：算法与制造", GREEN, ["品牌自研算法与 App；代工商未公开披露", "美国本土设厂：Oura 得州 Fort Worth、Ultrahuman 得州 Plano"]),
          ("下游：渠道与付费方", GOLD, ["直销 + 约 8,400 家零售门店；Oura 批发占比 27%→40%", "企业与支付方：200+ 机构、Essence 医保、美军合同（已终止）"]),
          ("服务与数据", WARM, ["会员 5.99 美元/月；接入 Dexcom 血糖、Natural Cycles 避孕"])]
y0 = 0.97
for h, c, items in layers:
    hgt = 0.05 + 0.07 * len(items)
    y0 -= hgt + 0.015
    box(ax, 0.0, y0, 0.2, hgt, h, fc=c, ec=c, tc="#FFFFFF", fs=11, bold=True)
    box(ax, 0.215, y0, 0.785, hgt, "", fc="#FFFFFF", ec=GREY, lw=0.9)
    for j, it in enumerate(items):
        ax.text(0.23, y0 + hgt - 0.06 - j * 0.07, it, fontsize=10.5, color=TXT, va="center")
D.save(fig, "fig4_chain.png")

# ---------- fig4 margin ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.1, 3.3), gridspec_kw={"width_ratios": [1.15, 1]})
per = ["FY2024", "FY2025", "2026 前 9 月"]
gm = [64.9, 51.9, 55.0]
a1.bar(per, gm, color=[BLUE, WARM, BLUE], width=0.55)
for i, v in enumerate(gm):
    a1.text(i, v + 1.5, f"{v:.1f}%", ha="center", fontsize=11.5, color=TXT)
a1.text(1.45, 70, "FY2025：Ring 4 电池批次\n保修费用 +8,440 万美元", ha="center", fontsize=10.5, color=WARM, va="center")
a1.set_ylim(0, 80); a1.set_title("Oura 综合毛利率", loc="left", fontsize=12.5, color=TXT); tidy(a1)
cats2 = ["会员\n毛利率", "会员收入\n占比", "每枚戒指\n收入（美元）"]
a2.axis("off")
rows = [("会员毛利率（2026 前 9 月）", "89%", ""), ("会员收入占比（前 9 月同比）", "16% → 20%", ""), ("每枚戒指收入（FY24 → 26 前 9 月）", "332 → 311 美元", ""), ("12 个月会员留存（加权平均）", "约 85%", "")]
for i, (k, v, n) in enumerate(rows):
    yy = 0.86 - i * 0.24
    a2.text(0.02, yy, k, fontsize=11, color=TXT2, transform=a2.transAxes)
    a2.text(0.02, yy - 0.105, v, fontsize=16, weight="bold", color=BLUE if i != 2 else WARM, transform=a2.transAxes)
    a2.text(0.98, yy - 0.105, n, fontsize=10, color=MUTED, ha="right", transform=a2.transAxes)
D.save(fig, "fig4_margin.png")

# ---------- fig5 adoption ----------
fig, ax = plt.subplots(figsize=(9.1, 3.3))
dev = [("智能手表", 43), ("智能体重秤", 13), ("联网血压计", 13), ("连续血糖仪", 9), ("智能戒指", 8)]
yy = np.arange(len(dev))[::-1]
ax.barh(yy, [v for _, v in dev], color=[GREY, GREY, GREY, GREY, BLUE], height=0.6)
for y_, (n, v) in zip(yy, dev):
    ax.text(v + 0.6, y_, f"{v}%", va="center", fontsize=11.5, color=TXT)
ax.set_yticks(yy); ax.set_yticklabels([n for n, _ in dev], fontsize=11.5)
ax.set_xlim(0, 60); ax.set_xlabel("美国成年人拥有比例（2025-12，n=8,000）")
ax.text(59, 1.6, "可穿戴设备主人追踪的指标\n运动 35% · 睡眠 26% · 心率 21%", ha="right", fontsize=11, color=TXT2, va="center")
tidy(ax, ygrid=False); ax.xaxis.grid(True); ax.set_axisbelow(True)
D.save(fig, "fig5_adoption.png")

# ---------- fig5 channels ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.1, 3.3), gridspec_kw={"width_ratios": [0.8, 1.2]})
a1.bar(["FY2024", "2026 前 9 月"], [27, 40], color=[GREY, BLUE], width=0.5)
for i, v in enumerate([27, 40]):
    a1.text(i, v + 1.2, f"{v}%", ha="center", fontsize=12, color=TXT)
a1.set_ylim(0, 50); a1.set_title("Oura 批发渠道收入占比", loc="left", fontsize=12.5); tidy(a1)
a2.axis("off")
evs = [("2024-10", "美军 DHA 授予 9,600 万美元戒指与服务合同", BLUE),
       ("2024-11", "Dexcom 投资 7,500 万美元，血糖数据接入 App", BLUE),
       ("2025-01", "Essence 医保计划向会员免费发放戒指", BLUE),
       ("2025-03", "DHA 以\"不再需要\"终止合同（WHOOP 曾抗议）", WARM),
       ("2025-08", "得州建厂服务国防业务，Palantir 关联引发隐私争议", WARM),
       ("2026-06", "Essence 增加睡眠呼吸暂停转诊流程", BLUE)]
for i, (t, s, c) in enumerate(evs):
    yy = 0.93 - i * 0.165
    a2.text(0.0, yy, t, fontsize=10.5, color=c, weight="bold", transform=a2.transAxes, va="center")
    a2.text(0.2, yy, s, fontsize=10.5, color=TXT, transform=a2.transAxes, va="center")
D.save(fig, "fig5_channels.png")

# ---------- fig6 accuracy ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.1, 3.3), gridspec_kw={"width_ratios": [1, 1]})
hr = [("Oura 4", 0.98, 0.99), ("Oura 3", 0.97, 0.97), ("WHOOP", 0.91, 0.94), ("Polar 等", 0.86, 0.87)]
x = np.arange(len(hr))
a1.bar(x - 0.18, [h[1] for h in hr], 0.34, color=BLUE, label="静息心率")
a1.bar(x + 0.18, [h[2] for h in hr], 0.34, color=GREEN, label="HRV")
a1.set_xticks(x); a1.set_xticklabels([h[0] for h in hr], fontsize=10.5); a1.set_ylim(0.7, 1.05)
a1.set_title("与 ECG 的一致性（CCC，纵轴从 0.7 起）", loc="left", fontsize=11.5); a1.legend(frameon=False, ncol=2, loc="upper right", fontsize=10); tidy(a1)
sl = [("睡眠/清醒\n（厂商，n=96）", 91.8, BLUE), ("四期分期\n（厂商，n=35）", 76.3, BLUE), ("四期分期\n（独立研究）", 53, WARM)]
a2.bar(range(3), [s[1] for s in sl], color=[s[2] for s in sl], width=0.55)
for i, s in enumerate(sl):
    a2.text(i, s[1] + 2, f"{s[1]:g}%", ha="center", fontsize=11.5, color=TXT)
a2.set_xticks(range(3)); a2.set_xticklabels([s[0] for s in sl], fontsize=10); a2.set_ylim(0, 110)
a2.set_title("Oura 睡眠判读与 PSG 一致率", loc="left", fontsize=11.5); tidy(a2)
D.save(fig, "fig6_accuracy.png")

# ---------- fig6 battery ----------
fig, ax = plt.subplots(figsize=(9.1, 3.3))
bat = [("Oura Ring 5", 10.2, 10.5, "6–9 天"), ("Oura Gen3", 15, 22, "4–7 天"), ("Galaxy Ring", 18, 23.5, "6–7 天"), ("Grepow 可定制范围", 6.2, 24, "")]
yy = np.arange(len(bat))[::-1]
for y_, (n, lo, hi, life) in zip(yy, bat):
    ax.plot([lo, hi], [y_, y_], color=BLUE if "Grepow" not in n else GREY, lw=9, solid_capstyle="butt")
    ax.text(hi + 0.6, y_, f"{lo:g}–{hi:g} mAh" + (f"　续航 {life}" if life else ""), va="center", fontsize=11, color=TXT)
ax.set_yticks(yy); ax.set_yticklabels([b[0] for b in bat], fontsize=11.5); ax.set_xlim(0, 42)
ax.set_xlabel("电池容量（mAh，随戒指尺寸变化）")
ax.text(41.5, 3.0, "参照：一部手机约 4,000–5,000 mAh", ha="right", fontsize=10.5, color=MUTED, va="center")
tidy(ax, ygrid=False); ax.xaxis.grid(True); ax.set_axisbelow(True)
D.save(fig, "fig6_battery.png")

# ---------- fig7 share ----------
fig, ax = plt.subplots(figsize=(9.1, 3.3))
groups = [("全球 2023\n（IDC）", {"Oura": 80, "Ultrahuman": 12, "其他": 8}),
          ("全球 2025 上半年\n（Omdia）", {"Oura": 74, "Ultrahuman": 9, "三星": 9, "RingConn": 5, "其他": 3}),
          ("美国 2024\n（IDC）", {"Oura": 63.3, "Ultrahuman": 11.5, "其他": 25.2}),
          ("美国 2025 年末\n（IDC）", {"Oura": 85, "其他": 15})]
colmap = {"Oura": BLUE, "Ultrahuman": WARM, "三星": GOLD, "RingConn": GREEN, "其他": GREY}
for i, (g, parts) in enumerate(groups):
    left = 0
    for k, v in parts.items():
        ax.barh(i, v, left=left, color=colmap[k], height=0.62, label=k if i == 1 else None)
        if v >= 8:
            ax.text(left + v / 2, i, f"{v:g}%", ha="center", va="center", fontsize=10.5, color="#FFFFFF" if k != "其他" else TXT)
        left += v
ax.set_yticks(range(4)); ax.set_yticklabels([g for g, _ in groups], fontsize=10.5); ax.invert_yaxis()
ax.set_xlim(0, 100); ax.set_xlabel("出货份额（%）"); ax.tick_params(length=0)
ax.legend(frameon=False, ncol=5, loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=10.5)
D.save(fig, "fig7_share.png")

# ---------- fig7 litigation ----------
fig, ax = plt.subplots(figsize=(9.1, 3.5))
lanes = ["Oura 对 RingConn\n/ Circular / Omate", "Oura 对 Ultrahuman", "三星与 Oura 互诉"]
items = [(0, "2024-06-25", "Circular 签许可"), (0, "2025-10-21", "RingConn、Omate 签许可"), (0, "2025-12-08", "RingConn 移出排除令"),
         (1, "2025-04-18", "ITC 初裁"), (1, "2025-08-21", "ITC 终裁：侵权"), (1, "2025-10-21", "排除令生效"),
         (1, "2026-03-06", "CBP 放行改款"), (1, "2026-10-22", "得州再诉"),
         (2, "2025-03-27", "三星确认之诉被驳回"), (2, "2025-11-19", "Oura 向 ITC 诉三星等"), (2, "2025-12-15", "三星反诉 Oura（ITC）")]
for lane in range(3):
    ax.axhline(lane, color=LIGHT, lw=10, zorder=0)
OFF = [0.3, -0.3, 0.3, -0.3, 0.3, -0.3, 0.3, -0.3, 0.3, -0.3, 0.3]
for k, (lane, ds, t) in enumerate(items):
    xd = d(ds); c = WARM if "排除令" in t or "侵权" in t or "再诉" in t else BLUE
    ax.plot(xd, lane, "o", color=c, ms=8, zorder=3)
    off = OFF[k]
    ax.text(xd, lane + off, t, ha="center", va="center", fontsize=10, color=TXT)
ax.set_yticks(range(3)); ax.set_yticklabels(lanes, fontsize=10.5); ax.set_ylim(2.6, -0.6)
ax.set_xlim(d("2024-04-01"), d("2027-01-15"))
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7])); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
ax.tick_params(length=0); ax.spines["left"].set_visible(False)
D.save(fig, "fig7_litigation.png")

# ---------- fig8 risk ----------
fig, ax = plt.subplots(figsize=(9.1, 3.6))
ax.axvspan(0.5, 1.0, ymin=0.5, ymax=1.0, color=WARM, alpha=0.08, lw=0)
risks = [(0.82, 0.86, "专利 / 进口禁令"), (0.66, 0.70, "电池鼓包与保修成本"), (0.70, 0.40, "睡眠准确性宣称诉讼"),
         (0.42, 0.62, "健康数据隐私事件"), (0.30, 0.82, "苹果入场"), (0.55, 0.30, "关税与供应链"),
         (0.25, 0.42, "医疗功能监管收紧"), (0.40, 0.18, "低价白牌冲击均价")]
for x_, y_, t in risks:
    c = WARM if x_ > 0.5 and y_ > 0.5 else BLUE
    ax.plot(x_, y_, "o", color=c, ms=11)
    ax.text(x_ + 0.02, y_ + 0.035, t, fontsize=11, color=TXT)
ax.set_xlim(0, 1.05); ax.set_ylim(0, 1.0)
ax.set_xlabel("未来 12–24 个月发生可能性（研究者判断）"); ax.set_ylabel("对行业影响")
ax.set_xticks([0.1, 0.5, 0.9]); ax.set_xticklabels(["低", "中", "高"]); ax.set_yticks([0.1, 0.5, 0.9]); ax.set_yticklabels(["低", "中", "高"])
ax.axvline(0.5, color=GREY, lw=0.8, ls="--"); ax.axhline(0.5, color=GREY, lw=0.8, ls="--"); tidy(ax, ygrid=False)
D.save(fig, "fig8_risk.png")
