"""贵州茅台经营分析（方向 4）幻灯片版图表。数据全部取自 drafts/moutai_fin/content/ 的取证稿（年报、季报原文）。
运行：FIG_OUT=drafts/moutai_fin/figs_deck python3 drafts/moutai_fin/make_figs.py"""
import os, sys
_R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(_R, "tools"))
import deckfig as D
from deckfig import plt, np, tidy, wrap_cjk, C, TXT, TXT2, MUTED, LIGHT, BLUE, WARM

GREY = "#B9B4A8"; GREEN = C[2]; GOLD = C[3]; DEEP = "#15212E"; LBLUE = "#8FA7C2"

def lab(ax, x, y, s, **k):
    kk = dict(ha="center", va="bottom", fontsize=10.5, color=TXT2); kk.update(k); ax.text(x, y, s, **kk)

# ---------- fig1_2 业务结构 ----------
fig, ax = plt.subplots(figsize=(9.1, 3.3))
rows = [("按产品", [("茅台酒", 1465.00, BLUE), ("其他系列酒", 222.75, GREY)]),
        ("按渠道", [("直销", 845.43, BLUE), ("批发代理", 842.32, GREY)]),
        ("按地区", [("国内", 1639.24, BLUE), ("国外", 48.50, GREY)])]
for i, (name, parts) in enumerate(rows):
    y = 2 - i; tot = sum(v for _, v, _ in parts); left = 0
    for j, (lb, v, c) in enumerate(parts):
        w = v / tot * 100
        ax.barh(y, w, left=left, color=c, height=0.58)
        txt = f"{lb} {v:,.2f} 亿 · {w:.1f}%"
        if w > 14:
            ax.text(left + w / 2, y, txt, ha="center", va="center", fontsize=11, color="#FFFFFF" if c == BLUE else TXT, weight="bold")
        else:
            ax.text(left + w + 1.2, y, txt, ha="left", va="center", fontsize=10.5, color=TXT2)
        left += w
    ax.text(-2, y, name, ha="right", va="center", fontsize=12, weight="bold", color=TXT)
ax.set_xlim(-16, 118); ax.set_ylim(-0.6, 2.6); ax.axis("off")
ax.text(50, -0.55, "2025 年主营业务收入 1687.75 亿元；三组口径各自合计相同", ha="center", va="center", fontsize=10, color=MUTED)
D.save(fig, "fig1_2_structure.png")

# ---------- fig2_1 收入与利润走势 ----------
fig, ax = plt.subplots(figsize=(9.1, 3.9))
yrs = ["2021", "2022", "2023", "2024", "2025", "2026\n前三季"]
tot = [1094.64, 1275.54, 1505.60, 1741.44, 1720.54, 1332.84]
npf = [524.60, 627.17, 747.34, 862.28, 823.20, 644.67]
gt = [None, 16.5, 18.0, 15.7, -1.2, 1.8]
x = np.arange(len(yrs))
cols = [BLUE] * 4 + [WARM, GREY]
ax.bar(x - 0.2, tot, 0.38, color=cols, label="营业总收入")
ax.bar(x + 0.2, npf, 0.38, color=[LBLUE] * 5 + ["#D6D2C8"], label="归母净利润")
for i in range(len(yrs)):
    lab(ax, x[i] - 0.2, tot[i] + 25, f"{tot[i]:,.0f}", fontsize=10.5, color=TXT)
    lab(ax, x[i] + 0.2, npf[i] + 25, f"{npf[i]:,.0f}", fontsize=10, color=TXT2)
    if gt[i] is not None:
        c = WARM if gt[i] < 0 else TXT2
        lab(ax, x[i] - 0.2, tot[i] + 130, f"{gt[i]:+.1f}%", fontsize=11, weight="bold", color=c)
ax.set_xticks(x); ax.set_xticklabels(yrs); ax.set_ylim(0, 2050); ax.set_ylabel("亿元")
ax.text(5, 1760, "2026 前三季\n不与全年相比", ha="center", va="bottom", fontsize=9.5, color=MUTED)
tidy(ax); ax.legend(frameon=False, loc="upper left", ncol=2)
D.save(fig, "fig2_1_trend.png")

# ---------- fig2_2 分产品 ----------
fig, ax = plt.subplots(figsize=(9.1, 3.6))
yrs = ["2023", "2024", "2025"]; x = np.arange(3)
mt = [1265.89, 1459.28, 1465.00]; se = [206.30, 246.84, 222.75]
gm = ["+17.4%", "+15.3%", "+0.4%"]; gs = ["+29.4%", "+19.7%", "−9.8%"]
ax.bar(x - 0.2, mt, 0.38, color=BLUE, label="茅台酒")
ax.bar(x + 0.2, se, 0.38, color=[GREY, GREY, WARM], label="其他系列酒")
for i in range(3):
    lab(ax, x[i] - 0.2, mt[i] + 20, f"{mt[i]:,.0f}  {gm[i]}", fontsize=10.5, color=TXT if i < 2 else WARM, weight="bold" if i == 2 else "normal")
    lab(ax, x[i] + 0.2, se[i] + 20, f"{se[i]:,.0f}  {gs[i]}", fontsize=10.5, color=TXT2 if i < 2 else WARM, weight="bold" if i == 2 else "normal")
ax.set_xticks(x); ax.set_xticklabels(yrs); ax.set_ylim(0, 1750); ax.set_ylabel("收入（亿元）")
tidy(ax); ax.legend(frameon=False, loc="upper left", ncol=2)
D.save(fig, "fig2_2_products.png")

# ---------- fig2_3 渠道 ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.1, 3.6), gridspec_kw=dict(width_ratios=[1.15, 1], wspace=0.3))
per = ["2023", "2024", "2025", "2025\n前三季", "2026\n前三季"]
share = [45.7, 43.9, 50.1, 43.3, 56.4]
x = np.arange(5)
a1.plot(x[:3], share[:3], "-o", color=BLUE, lw=2.2, ms=7)
a1.plot(x[3:], share[3:], "o", color=BLUE, ms=7); a1.plot(x[3:], share[3:], color=BLUE, lw=2.2, ls=(0, (4, 2)))
for i in range(5):
    lab(a1, x[i], share[i] + (1.6 if i != 3 else -1.8), f"{share[i]:.1f}%", fontsize=11, color=TXT, weight="bold" if i == 4 else "normal", va="bottom" if i != 3 else "top")
a1.axhline(50, color=GREY, lw=0.9, ls=(0, (3, 3))); a1.text(4.35, 50.6, "50%", fontsize=9.5, color=MUTED, ha="right")
a1.set_xticks(x); a1.set_xticklabels(per, fontsize=9.5); a1.set_ylim(35, 62); a1.set_ylabel("直销占主营收入比例（%）")
tidy(a1)
imt = [118.83, 223.74, 200.24, 130.31, 126.92, 585.62]
pl = ["2022", "2023", "2024", "2025", "2025\n前三季", "2026\n前三季"]
xx = np.arange(6)
a2.bar(xx, imt, 0.6, color=[BLUE] * 4 + [GREY, WARM])
for i in range(6):
    lab(a2, xx[i], imt[i] + 10, f"{imt[i]:,.0f}", fontsize=10.5, color=TXT)
a2.set_xticks(xx); a2.set_xticklabels(pl, fontsize=9.5); a2.set_ylim(0, 680); a2.set_ylabel("i 茅台酒类收入（亿元）")
a2.text(2.0, 400, "2026 年起含经销商\n经平台代售的收入，\n口径不可比", ha="center", va="bottom", fontsize=9.5, color=WARM, linespacing=1.4)
tidy(a2)
D.save(fig, "fig2_3_channels.png")

# ---------- fig3_1 毛利率 ----------
fig, ax = plt.subplots(figsize=(9.1, 3.4))
yrs = ["2023", "2024", "2025"]; x = np.arange(3)
ser = {"茅台酒": ([94.12, 94.06, 93.53], BLUE), "酒类合计": ([92.11, 92.01, 91.23], TXT2), "其他系列酒": ([79.76, 79.87, 76.11], WARM)}
for k, (v, c) in ser.items():
    ax.plot(x, v, "-o", color=c, lw=2.2, ms=7, label=k)
    for i in range(3):
        if k == "酒类合计": lab(ax, x[i], v[i] - 0.8, f"{v[i]:.2f}", fontsize=10.5, color=c, va="top")
        else: lab(ax, x[i], v[i] + 0.7, f"{v[i]:.2f}", fontsize=10.5, color=c)
ax.set_xticks(x); ax.set_xticklabels(yrs); ax.set_ylim(72, 98); ax.set_ylabel("毛利率（%）")
ax.text(2.05, 86, "系列酒 −3.76 pct\n（降档走量）", fontsize=10.5, color=WARM, va="center")
tidy(ax); ax.legend(frameon=False, loc="lower left", ncol=3)
D.save(fig, "fig3_1_margin.png")

# ---------- fig3_2 费用率 ----------
fig, ax = plt.subplots(figsize=(9.1, 3.4))
yrs = ["2022", "2023", "2024", "2025"]; x = np.arange(4)
ser = {"税金及附加": ([14.90, 15.05, 15.76, 16.20], TXT2), "管理费用": ([7.26, 6.59, 5.45, 4.93], BLUE), "销售费用": ([2.66, 3.15, 3.30, 4.30], WARM)}
for k, (v, c) in ser.items():
    ax.plot(x, v, "-o", color=c, lw=2.2, ms=7, label=k)
    for i in range(4):
        if k == "销售费用": lab(ax, x[i], v[i] - 0.5, f"{v[i]:.2f}", fontsize=10.5, color=c, va="top")
        else: lab(ax, x[i], v[i] + 0.45, f"{v[i]:.2f}", fontsize=10.5, color=c)
ax.set_xticks(x); ax.set_xticklabels(yrs); ax.set_ylim(0, 19); ax.set_ylabel("占营业收入比例（%）")
ax.text(3.08, 2.2, "+28.6%（72.53 亿）", fontsize=10.5, color=WARM, va="center")
tidy(ax); ax.legend(frameon=False, loc="center left", bbox_to_anchor=(0.0, 0.6), ncol=1)
D.save(fig, "fig3_2_expense.png")

# ---------- fig4_1 现金流分解 ----------
fig, ax = plt.subplots(figsize=(9.1, 3.7))
yrs = ["2022", "2023", "2024", "2025"]; x = np.arange(4)
ocf = [366.99, 665.93, 924.64, 615.22]; dep = [-89.16, -8.10, 110.60, -50.99]
core = [o - d for o, d in zip(ocf, dep)]
npf = [627.17, 747.34, 862.28, 823.20]
ax.bar(x, core, 0.52, color=BLUE, label="剔除财务公司存款后的经营现金流")
ax.bar(x, dep, 0.52, bottom=[c if d > 0 else 0 for c, d in zip(core, dep)], color=[WARM if d < 0 else GREY for d in dep], label="客户存款和同业存放款项净增加额")
for i in range(4):
    lab(ax, x[i], max(core[i], ocf[i]) + 18, f"报表 {ocf[i]:,.0f}", fontsize=10.5, color=TXT, weight="bold")
    lab(ax, x[i] + 0.33, core[i] / 2, f"{core[i]:,.0f}", fontsize=10, color=BLUE, ha="left", va="center")
    lab(ax, x[i] + 0.33, (core[i] + dep[i] / 2) if dep[i] > 0 else dep[i] / 2, f"{dep[i]:+,.0f}", fontsize=10, color=WARM if dep[i] < 0 else TXT2, ha="left", va="center")
ax.axhline(0, color=TXT2, lw=0.8)
ax.set_xticks(x); ax.set_xticklabels(yrs); ax.set_ylim(-140, 1080); ax.set_ylabel("亿元")
tidy(ax); ax.legend(frameon=False, loc="upper left", fontsize=9.5)
D.save(fig, "fig4_1_cashflow.png")

# ---------- fig4_2 合同负债 ----------
fig, ax = plt.subplots(figsize=(9.1, 3.4))
pts = ["2022-12", "2023-12", "2024-12", "2025-09", "2025-12", "2026-06", "2026-09"]
cl = [154.72, 141.26, 95.92, 77.49, 80.07, 31.78, 20.84]
x = np.arange(7)
ax.bar(x, cl, 0.58, color=[BLUE] * 5 + [WARM, WARM])
for i in range(7):
    lab(ax, x[i], cl[i] + 3, f"{cl[i]:.2f}", fontsize=11, color=TXT, weight="bold" if i == 6 else "normal")
ax.axhline(70, color=GREY, lw=0.9, ls=(0, (3, 3))); ax.text(6.4, 72, "≈ 一个月批发收入（70 亿）", fontsize=9.5, color=MUTED, ha="right")
ax.set_xticks(x); ax.set_xticklabels(pts); ax.set_ylim(0, 180); ax.set_ylabel("合同负债期末余额（亿元）")
tidy(ax)
D.save(fig, "fig4_2_contract.png")

# ---------- fig5_2 同业增速 ----------
fig, ax = plt.subplots(figsize=(9.1, 3.6))
names = ["贵州茅台", "山西汾酒", "泸州老窖", "五粮液"]
g25 = [-1.2, 7.5, -17.5, -54.6]; g26 = [2.0, -13.8, -36.6, 7.3]
y = np.arange(4)[::-1]
ax.barh(y + 0.2, g25, 0.36, color=[BLUE, GREY, GREY, GREY], label="2025 年营业收入同比")
ax.barh(y - 0.2, g26, 0.36, color=[BLUE, WARM, WARM, GREY], label="2026 年 1–9 月同比")
for i in range(4):
    for yy, v in ((y[i] + 0.2, g25[i]), (y[i] - 0.2, g26[i])):
        ax.text(v + (1.2 if v >= 0 else -1.2), yy, f"{v:+.1f}%", va="center", ha="left" if v >= 0 else "right", fontsize=10.5, color=TXT)
ax.text(15.5, y[3] - 0.2, "重述基数；2025 年为重述口径", va="center", fontsize=9.5, color=MUTED)
ax.axvline(0, color=TXT2, lw=0.8)
ax.set_yticks(y); ax.set_yticklabels(names, fontsize=11); ax.set_xlim(-66, 36); ax.set_xlabel("营业收入同比（%）")
tidy(ax, ygrid=False); ax.xaxis.grid(True); ax.set_axisbelow(True); ax.legend(frameon=False, loc="upper right")
D.save(fig, "fig5_2_peers.png")

# ---------- fig6_2 价格节点 ----------
fig, ax = plt.subplots(figsize=(9.1, 3.7))
# 合同价阶梯（年份小数）
steps = [(2023.0, 969), (2023.83, 1169), (2026.25, 1269), (2026.55, 1369), (2026.85, 1369)]
sx = [s[0] for s in steps]; sy = [s[1] for s in steps]
ax.step(sx, sy, where="post", color=BLUE, lw=2.4, label="飞天合同价 / 出厂价（元/瓶）")
for xx, yy, t in [(2023.1, 969, "969"), (2024.0, 1169, "1169（2023-11）"), (2026.27, 1180, "1269（2026-03）"), (2026.57, 1369, "1369（2026-07）")]:
    ax.text(xx, yy + 28, t, fontsize=10.5, color=BLUE, weight="bold")
# 批价散点
bp = [(2024.0, 2700, "约 2700", True), (2025.0, 2220, "2220", False), (2025.48, 1800, "跌破 1800", False), (2025.82, 1690, "1690", False),
      (2025.9, 1590, "", False), (2025.95, 1485, "1485", False), (2026.08, 1660, "1660", False), (2026.55, 1655, "1650–1660", False)]
ax.plot([b[0] for b in bp], [b[1] for b in bp], "-o", color=WARM, lw=1.8, ms=6, label="散瓶批价（今日酒价，媒体转引）")
for xx, yy, t, weak in bp:
    if not t: continue
    if t == "1485": ax.text(xx + 0.02, yy - 45, t, fontsize=9.5, color=WARM, ha="left", va="top")
    elif t == "1690": ax.text(xx - 0.03, yy + 40, t, fontsize=9.5, color=WARM, ha="right")
    elif t == "1660": ax.text(xx + 0.04, yy + 40, t, fontsize=9.5, color=WARM, ha="left")
    else: ax.text(xx + 0.03, yy + 40, t, fontsize=9.5, color=WARM if not weak else MUTED, ha="left")
ax.axhline(1499, color=GREY, lw=0.9, ls=(0, (3, 3))); ax.text(2023.02, 1515, "自营零售价 1499（至 2026-03）", fontsize=9.5, color=MUTED)
ax.text(2025.0, 2240, "", fontsize=1)
ax.annotate("价差 1051 元（47%）", xy=(2025.0, 1700), fontsize=10, color=TXT2, ha="center")
ax.annotate("价差 286 元（17%）", xy=(2026.35, 1960), fontsize=10, color=TXT2, ha="center", va="bottom")
ax.set_xlim(2022.9, 2027.0); ax.set_ylim(800, 2950); ax.set_ylabel("元 / 瓶（53%vol 500ml）")
ax.set_xticks([2023, 2024, 2025, 2026, 2027]); ax.set_xticklabels(["2023", "2024", "2025", "2026", "2027"])
tidy(ax); ax.legend(frameon=False, loc="upper right")
D.save(fig, "fig6_2_prices.png")

# ---------- fig6_3 情景 ----------
fig, ax = plt.subplots(figsize=(9.1, 3.5))
names = ["2025 实际", "悲观\n茅台酒 +1.0%", "基准\n茅台酒 +2.2%", "乐观\n茅台酒 +4.0%"]
vals = [1720.54, 1736.3, 1753.5, 1780.2]; g = ["", "+0.9%", "+1.9%", "+3.5%"]
x = np.arange(4)
ax.bar(x, vals, 0.55, color=[TXT2, GREY, BLUE, GREY])
for i in range(4):
    lab(ax, x[i], vals[i] + 4, f"{vals[i]:,.1f}  {g[i]}", fontsize=11, color=TXT, weight="bold" if i == 2 else "normal")
ax.axhline(1776.12, color=WARM, lw=1.2, ls=(0, (4, 2))); ax.text(-0.42, 1778, "国信证券 2026E 1776.1", fontsize=10, color=WARM, ha="left", va="bottom")
ax.axhline(1807.43, color=WARM, lw=1.2, ls=(0, (4, 2))); ax.text(-0.42, 1809, "华泰研究 2026E 1807.4", fontsize=10, color=WARM, ha="left", va="bottom")
ax.set_xticks(x); ax.set_xticklabels(names, fontsize=10.5); ax.set_ylim(1650, 1850); ax.set_ylabel("FY2026 营业总收入（亿元，从 1650 起）")
tidy(ax)
D.save(fig, "fig6_3_scenarios.png")
print("done")
