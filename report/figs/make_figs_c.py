from common import *
from matplotlib.patches import Patch

GREY_D = "#8a8984"; GREY_L = "#c8c7c1"; ACC = C[0]

# ---------- fig2_2_forecast: institutional forecast paths (log) ----------
fig, ax = plt.subplots(figsize=(6.3, 3.3))
series = [
    # name, base_year, base_value(bn USD), cagr, end_year, end_value, color, wide?
    ("MarketsandMarkets（宽口径，含编程 API）", 2025, 8.14, 0.481, 2032, 127.05, ACC, True),
    ("Grand View Research（工具 + 服务）", 2024, 26.03 / (1.271 ** 6), 0.271, 2030, 26.03, "#5f93dd", True),
    ("Precedence Research（窄口径）", 2025, 0.05025, 0.2531, 2035, 0.4797, GREY_D, False),
    ("Global Industry Analysts（窄口径）", 2024, 0.0259, 0.248, 2030, 0.0979, GREY_L, False),
]
for name, y0, v0, g, y1, v1, c, wide in series:
    ys = np.arange(y0, y1 + 1)
    vs = v0 * (1 + g) ** (ys - y0)
    ax.plot(ys, vs, ls="--", color=c, lw=1.6 if wide else 1.2, zorder=2)
    filled = name.startswith("Grand") is False
    ax.plot([y0], [v0], "o", color=c if filled else "white", mec=c, mew=1.4, ms=6, zorder=3)
    ax.plot([y1], [v1], "o", color="white", mec=c, mew=1.4, ms=6, zorder=3)
    lbl = f"{v1:.3g}" if v1 < 1 else f"{v1:,.0f}" if v1 > 10 else f"{v1:.1f}"
    ax.annotate(f"{lbl}（{y1}）  {name}", (y1, v1), xytext=(7, 0), textcoords="offset points", va="center", fontsize=6.6, color=c if wide else TXT2)
# bottom-up marker
ax.plot([2026.5], [8.725], marker="D", color=C[1], ms=7, zorder=4)
ax.annotate("头部六家厂商年化收入\n合计 ≈87 亿美元\n（2026 年年中，\n研究者计算）", (2026.5, 8.725), xytext=(2025.6, 1.1), textcoords="data", fontsize=6.8, color=C[1], va="center", ha="left", linespacing=1.3,
            arrowprops=dict(arrowstyle="-", color=C[1], lw=0.8))
ax.set_yscale("log"); ax.set_ylim(0.015, 400); ax.set_xlim(2023.6, 2045)
ax.set_xticks(range(2024, 2037, 2)); ax.spines["bottom"].set_bounds(2023.6, 2036)
ax.set_ylabel("十亿美元（对数坐标）")
tidy(ax)
ax.annotate("", xy=(2030.15, 58), xytext=(2030.15, 0.16), arrowprops=dict(arrowstyle="<->", color=TXT2, lw=0.8))
ax.text(2030.35, 2.2, "2030 年\n相差两个\n数量级以上", fontsize=6.8, color=TXT2, va="center")
ax.text(2023.7, 250, "● 基准年数值   ○ 机构预测终点   - - 按 CAGR 插值（研究者计算）", fontsize=6.5, color=MUTED)
save(fig, "fig2_2_forecast.png")

# ---------- fig2_bottomup ----------
fig, ax = plt.subplots(figsize=(6.3, 3.2))
comp = [("Cursor", 40.0), ("Claude Code", 25.0), ("Cognition", 9.0), ("Lovable", 6.0), ("Replit", 5.25), ("Base44", 2.0)]
shades = ["#143c6e", "#1f5aa3", "#2a78d6", "#5f93dd", "#8db3e7", "#b7d0f0"]
bottom = 0
for (n, v), c in zip(comp, shades):
    ax.bar(0, v, bottom=bottom, color=c, width=0.55, edgecolor="white", lw=1.2)
    dy = {"Base44": 1.6, "Replit": -0.6}.get(n, 0)
    ax.text(0.31, bottom + v / 2 + dy, f"{n} {v:g}", va="center", fontsize=7, color=TXT)
    bottom += v
ax.text(0, bottom + 2, f"≈{bottom:.0f}", ha="center", fontsize=9, weight="bold", color=TXT)
# copilot range
ax.bar(1.2, 22 - 5.6, bottom=5.6, color="white", edgecolor=ACC, hatch="////", width=0.4, lw=0.8)
ax.text(1.2, 23.5, "5.6–22", ha="center", fontsize=8, color=TXT)
# agency estimates
ag = [("MarketsandMarkets", 81.4, GREY_D), ("Precedence", 0.503, GREY_L), ("GIA", 0.259, GREY_L)]
for i, (n, v, c) in enumerate(ag):
    x = 2.5 + i * 0.9
    ax.bar(x, v, color=c, width=0.55)
    ax.text(x, v + 2, f"{v:.2g}" if v < 1 else f"{v:.1f}", ha="center", fontsize=8, color=TXT)
ax.set_xticks([0, 1.2, 2.5, 3.4, 4.3])
ax.set_xticklabels(["头部六家厂商\n年化收入合计\n（2026 年年中）", "GitHub Copilot\n订阅收入估算\n（未计入合计）", "MarketsandMarkets\n2025 年全年\n（宽口径）", "Precedence\n2025 年\n（窄口径）", "Global Industry\nAnalysts 2024\n（窄口径）"], fontsize=6.6)
ax.set_ylabel("亿美元"); ax.set_ylim(0, 100); ax.set_xlim(-0.5, 4.8)
tidy(ax)
ax.axvline(1.85, color="#dedcd6", lw=0.8)
ax.text(0.6, 95, "自下而上：厂商收入", ha="center", fontsize=7.5, color=ACC, weight="bold")
ax.text(3.4, 95, "自上而下：机构估计", ha="center", fontsize=7.5, color=GREY_D, weight="bold")
ax.text(3.85, 14, "窄口径数值\n不足 1 亿美元，\n在本图中几乎不可见", fontsize=6.5, color=TXT2, ha="center")
save(fig, "fig2_bottomup.png")

# ---------- fig1_map: industry landscape map ----------
fig, ax = blank(6.3, 4.9)
cols = ["IDE 内嵌助手", "AI 原生 IDE", "终端 / CLI 智能体", "云端异步智能体", "一体化应用平台"]
rows = ["模型厂商", "平台与\n互联网大厂", "独立\n创业公司", "开源与社区"]
cells = {
 (0, 0): ["Gemini Code Assist · 谷歌"], (0, 1): ["Antigravity · 谷歌"],
 (0, 2): ["Claude Code · Anthropic", "Codex CLI · OpenAI", "Antigravity CLI · 谷歌"], (0, 3): ["Codex cloud · OpenAI", "Jules · 谷歌"],
 (1, 0): ["GitHub Copilot · 微软", "*Qoder CN · 阿里（原通义灵码）", "*CodeBuddy · 腾讯", "*文心快码 · 百度"], (1, 1): ["Kiro · AWS", "*Trae · 字节跳动", "*Qoder · 阿里"],
 (1, 3): ["Copilot 云端代理 · 微软"], (1, 4): ["Base44 · Wix", "v0 · Vercel", "*秒哒 · 百度"],
 (2, 1): ["Cursor · SpaceX（2026-08 起）", "Devin Desktop · Cognition"], (2, 3): ["Devin · Cognition"],
 (2, 4): ["Lovable", "Replit", "Bolt.new · StackBlitz", "Emergent"],
 (3, 0): ["Cline"], (3, 2): ["OpenCode", "Aider"], (3, 4): ["bolt.diy"],
}
x0, y0, cw, rh = 0.105, 0.07, 0.179, 0.2
for j, c in enumerate(cols):
    ax.add_patch(Rectangle((x0 + cw * j + 0.002, 0.845), cw - 0.004, 0.065, fc="#14365F", ec="none"))
    ax.text(x0 + cw * j + cw / 2, 0.8775, c, ha="center", va="center", fontsize=7, color="white", weight="bold")
RH = [0.175, 0.24, 0.24, 0.115]
YS = [y0 + sum(RH[i + 1:]) for i in range(4)]
for i, r in enumerate(rows):
    y = YS[i]; rh = RH[i]
    ax.add_patch(Rectangle((0, y + 0.003), x0 - 0.006, rh - 0.006, fc=LIGHT, ec="none"))
    ax.text((x0 - 0.006) / 2, y + rh / 2, r, ha="center", va="center", fontsize=6.8, weight="bold", color="#14365F", linespacing=1.3)
    for j in range(5):
        x = x0 + cw * j
        ax.add_patch(Rectangle((x + 0.002, y + 0.003), cw - 0.004, rh - 0.006, fc="white", ec="#e2e1dc", lw=0.6))
        if not cells.get((i, j)): ax.text(x + cw / 2, y + rh / 2, "—", ha="center", va="center", fontsize=7, color="#d0cfca")
        for k, it in enumerate(cells.get((i, j), [])):
            cn = it.startswith("*"); it = it.lstrip("*")
            name, _, owner = it.partition(" · ")
            top = y + rh - 0.009 - k * 0.0545
            h = 0.048 if owner else 0.03
            ax.add_patch(FancyBboxPatch((x + 0.007, top - h), cw - 0.014, h, boxstyle="round,pad=0,rounding_size=0.005", fc="#fdf1ec" if cn else "#eef4fb", ec="none"))
            ax.text(x + 0.013, top - (0.0125 if owner else 0.015), name, fontsize=6, va="center", color=TXT, weight="bold")
            if owner: ax.text(x + 0.013, top - 0.0355, owner, fontsize=5.4, va="center", color=C[1] if cn else TXT2)
ax.set_ylim(0, 0.915)
for xx, fc, t in [(0.105, "#eef4fb", "海外厂商"), (0.21, "#fdf1ec", "中国厂商")]:
    ax.add_patch(FancyBboxPatch((xx, 0.014), 0.025, 0.024, boxstyle="round,pad=0,rounding_size=0.004", fc=fc, ec="none"))
    ax.text(xx + 0.032, 0.026, t, fontsize=6, va="center", color=TXT2)
ax.text(0.345, 0.026, "—  该类别暂无代表产品", fontsize=6, va="center", color=TXT2)
save(fig, "fig1_map.png")

# ---------- fig2_3_arr: direct labels, single accent ----------
import datetime as dt
import matplotlib.dates as mdates
def d(s): return dt.date.fromisoformat(s)
fig, ax = plt.subplots(figsize=(6.3, 3.2))
series = [
 ("Cursor", [("2025-01-15", 0.1), ("2025-03-15", 0.2), ("2025-06-05", 0.5), ("2025-11-13", 1.0), ("2026-02-15", 2.0), ("2026-05-21", 3.0), ("2026-06-09", 4.0)], ACC, 2.4),
 ("Claude Code（匿名信源）", [("2025-10-15", 1.0), ("2026-02-12", 2.5)], "#5f93dd", 1.6),
 ("Cognition", [("2025-07-14", 0.082), ("2026-05-27", 0.492), ("2026-09-08", 0.9)], GREY_D, 1.4),
 ("Lovable", [("2024-12-15", 0.004), ("2025-07-15", 0.1), ("2025-12-01", 0.2), ("2026-02-15", 0.4), ("2026-06-09", 0.5), ("2026-08-31", 0.6)], C[1], 1.6),
 ("Replit（含 Sacra 估计）", [("2025-06-15", 0.1), ("2025-12-15", 0.265), ("2026-04-15", 0.525)], GREY_L, 1.4),
]
offs = {"Cursor": 2, "Claude Code（匿名信源）": 9, "Cognition": 2, "Lovable": -9, "Replit（含 Sacra 估计）": 9}
for name, pts, c, lw in series:
    xs = [d(a) for a, b in pts]; ys = [b for a, b in pts]
    ax.plot(xs, ys, "-", color=c, lw=lw); ax.plot(xs, ys, "o", color=c, ms=3.5)
    v = ys[-1]; lbl = f"{v*10:.0f} 亿" if v >= 1 else f"{v*10:.1f} 亿".replace(".0 亿", " 亿")
    if name.startswith("Replit"):
        ax.annotate(f"Replit  {lbl}（含 Sacra 估计）", (xs[-1], v), xytext=(3, -18), textcoords="offset points", va="center", ha="left", fontsize=7, color=GREY_D)
        continue
    left = name.startswith("Claude")
    ax.annotate(f"{name}  {lbl}", (xs[-1], v), xytext=(-6 if left else 6, (10 if name.startswith("Claude") else 4) if left else offs[name]), textcoords="offset points", va="center", ha="right" if left else "left", fontsize=7, color=c if c not in (GREY_L,) else GREY_D, weight="bold" if name == "Cursor" else "normal")
ax.annotate("Cursor 约 17 个月增长 40 倍", (d("2025-01-20"), 2.2), fontsize=7.5, color=ACC, ha="left", weight="bold")
ax.set_ylabel("年化收入（十亿美元，对数）"); ax.set_yscale("log"); ax.set_ylim(0.003, 8)
ax.set_xlim(d("2024-11-15"), d("2027-05-01"))
ax.set_xticks([d("2025-01-01"), d("2025-07-01"), d("2026-01-01"), d("2026-07-01")]); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
ax.spines["bottom"].set_bounds(mdates.date2num(d("2024-11-15")), mdates.date2num(d("2026-10-15")))
tidy(ax)
save(fig, "fig2_3_arr.png")

# ---------- fig3_3_swebench: direct labels ----------
fig, ax = plt.subplots(figsize=(6.3, 3.0))
pts = [("2024-06", 33.4), ("2024-08", 33.2), ("2024-10", 49.0), ("2025-02", 62.3), ("2025-09", 77.2), ("2025-11", 80.9), ("2026-02", 80.8), ("2026-04", 88.7), ("2026-05", 88.6), ("2026-06", 95.0)]
names = ["Claude 3.5 Sonnet", "GPT-4o", "Claude 3.5 Sonnet（新）", "Claude 3.7 Sonnet", "Claude Sonnet 4.5", "Claude Opus 4.5", "Claude Opus 4.6", "GPT-5.5", "Claude Opus 4.8", "Claude Fable 5"]
xs = [d(p + "-15") for p, _ in pts]; ys = [v for _, v in pts]
ax.plot(xs, ys, "-o", color=ACC, lw=2, ms=3.5)
for i, off in ((0, (4, -12)), (3, (-6, 8)), (4, (-8, 8)), (9, (-4, 7))):
    ax.annotate(f"{names[i]} {ys[i]:g}%", (xs[i], ys[i]), xytext=off, textcoords="offset points", ha="left" if i == 0 else ("right" if i in (3, 4) else "center"), fontsize=6.2, color=TXT2)
ax.text(d("2024-07-01"), 92, "SWE-bench Verified 顶分（厂商自报）", fontsize=7, color=ACC, weight="bold")
ax.plot([d("2025-09-15"), d("2026-05-15")], [23.3, 77.8], "-s", color=C[1], lw=1.8, ms=4)
ax.annotate("SWE-bench Pro 公开集顶分\n23.3% → 77.8%", (d("2026-05-15"), 77.8), xytext=(8, -16), textcoords="offset points", fontsize=7, color=C[1], weight="bold", ha="left")
ax.plot([d("2025-09-15")], [17.8], "D", color=C[7], ms=5)
ax.annotate("Pro 商业私有仓库 17.8%（Opus 4.1）", (d("2025-09-15"), 17.8), xytext=(8, -3), textcoords="offset points", fontsize=6.5, color=C[7])
ax.set_ylim(0, 105); ax.set_ylabel("通过率（%）")
ax.set_xlim(d("2024-04-01"), d("2026-12-01"))
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7])); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
tidy(ax)
save(fig, "fig3_3_swebench.png")
