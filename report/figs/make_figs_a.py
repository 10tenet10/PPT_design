from common import *
import matplotlib.ticker

# ---------- fig1_1 boundary ----------
fig, ax = blank(6.3, 3.9)
# core
box(ax, 0.28, 0.30, 0.44, 0.42, "", fc="#e9f1fc", ec=C[0], lw=1.4, rounding=0.03)
ax.text(0.50, 0.68, "AI 编程工具行业（本报告范围）", ha="center", fontsize=9, weight="bold", color=C[0])
items = ["IDE 内嵌助手", "AI 原生 IDE", "终端/CLI 智能体", "云端异步智能体", "一体化自然语言\n应用平台"]
xs = [0.305, 0.385, 0.465, 0.545, 0.625]
for x, t in zip(xs, items):
    box(ax, x, 0.36, 0.075, 0.22, t, fc="white", ec=C[0], fs=6.5)
# upstream
box(ax, 0.02, 0.76, 0.96, 0.17, "", fc=LIGHT, ec="#c8c7c1", rounding=0.02)
ax.text(0.5, 0.905, "上游投入（产业链分析，不计入市场规模）", ha="center", fontsize=8, color=TXT2)
for x, t in zip([0.08, 0.36, 0.64], ["基础模型（Anthropic、OpenAI、Google、\nDeepSeek、Qwen、Kimi、GLM）", "算力与云（NVIDIA、AWS、Azure、GCP、\n阿里云、火山引擎）", "模型厂商自营编程产品\n（Claude Code、Codex、Gemini Code Assist）"]):
    box(ax, x, 0.78, 0.26, 0.10, t, fc="white", ec="#c8c7c1", fs=6.5)
arrow(ax, 0.5, 0.76, 0.5, 0.725, color="#8a8984")
ax.text(0.90, 0.735, "自营产品计入行业", fontsize=6.5, color=TXT2, ha="right")
# left: traditional tools (base)
box(ax, 0.02, 0.30, 0.22, 0.42, "传统开发工具\n（运行基础，配套环节）\n\nGit / GitHub\nCI/CD、测试框架\n可观测性、IDE", fc=LIGHT, ec="#c8c7c1", fs=7)
arrow(ax, 0.24, 0.51, 0.28, 0.51, color="#8a8984", style="<|-|>")
# right: substitutes
box(ax, 0.76, 0.30, 0.22, 0.42, "替代品\n\n低代码 / 无代码平台\n直接使用 ChatGPT/Claude\n外包与自由职业者", fc="#fdf1ec", ec=C[1], fs=7)
arrow(ax, 0.72, 0.51, 0.76, 0.51, color=C[1], style="<|-|>", ls="--")
ax.text(0.74, 0.545, "融合中\n(Wix→Base44)", ha="center", fontsize=6, color=C[1])
# downstream
box(ax, 0.02, 0.05, 0.96, 0.17, "", fc=LIGHT, ec="#c8c7c1", rounding=0.02)
ax.text(0.5, 0.195, "下游用户", ha="center", fontsize=8, color=TXT2)
for x, t, fc in zip([0.06, 0.30, 0.54, 0.78], ["企业研发团队", "专业独立开发者", "创业团队", "低编程基础用户\n（本报告重点细分）"], ["white", "white", "white", "#fff3d6"]):
    box(ax, x, 0.07, 0.20, 0.10, t, fc=fc, ec="#c8c7c1" if fc == "white" else C[3], fs=6.5)
arrow(ax, 0.5, 0.30, 0.5, 0.225, color="#8a8984")
save(fig, "fig1_1_boundary.png")

# ---------- fig1_2 framework (v3) ----------
fig, ax = blank(6.3, 3.0)
steps = ["第一章\n行业定义\n与研究框架", "第二章\n行业发展\n与市场规模", "第三章\n宏观环境\n（PEST）", "第四章\n产业链与\n价值分配", "第五章\n用户需求\n与市场细分", "第六章\n技术与\n产品供给", "第七章\n竞争格局\n与商业模式", "第八章\n趋势、风险\n与行业洞察"]
n = len(steps); L0, R0 = 0.01, 0.99; w = 0.106; gap = (R0 - L0 - n * w) / (n - 1)
for i, s_ in enumerate(steps):
    x = L0 + i * (w + gap)
    fc = "#e9f1fc" if i in (4, 5) else "white"
    box(ax, x, 0.56, w, 0.32, s_, fc=fc, ec=C[0] if i in (4, 5) else "#9a9a94", fs=6.6, tc=TXT)
    if i < n - 1:
        arrow(ax, x + w, 0.72, x + w + gap, 0.72, color="#6f6e69", mutation=7)
ax.text(0.5, 0.94, "边界与发展 → 外部驱动 → 产业链 → 需求 → 供给 → 竞争 → 趋势与判断（阴影为重点细分所在章节）", ha="center", va="center", fontsize=7, color=TXT2)
ys = ["事实与数据\n（描述层）", "作用机制\n（解释层）", "行业影响", "研究判断\n（判断层）"]
for i, t in enumerate(ys):
    box(ax, 0.06 + i * 0.235, 0.22, 0.19, 0.16, t, fc=LIGHT, ec="#c8c7c1", fs=7, tc=TXT)
    if i < 3:
        arrow(ax, 0.25 + i * 0.235, 0.30, 0.295 + i * 0.235, 0.30, color="#6f6e69", mutation=6)
ax.text(0.5, 0.445, "各章统一的分析深度标准", ha="center", va="center", fontsize=7.5, color=TXT, weight="bold")
ax.text(0.5, 0.10, "证据规则：区分实际值 / 估计 / 预测 / 厂商自述 / 研究推断；不混用使用率、依赖率与付费率；\n不相加不同口径的市场规模", ha="center", va="center", fontsize=6.8, color=TXT2, linespacing=1.4)
save(fig, "fig1_2_framework.png")

# ---------- fig2_1 timeline ----------
fig, ax = plt.subplots(figsize=(6.3, 4.2))
ax.set_xlim(2021.2, 2027.0); ax.set_ylim(-1, 1); ax.axis("off")
ax.axhline(0, color="#9a9a94", lw=1.2, zorder=1)
for yr in range(2021, 2027):
    ax.plot([yr + 0.5, yr + 0.5], [-0.04, 0.04], color="#9a9a94", lw=1)
    ax.text(yr + 0.5, -0.10, str(yr), ha="center", fontsize=8, color=TXT2)
# phases
for (a, b, t, c) in [(2021.3, 2023.0, "补全阶段", C[3]), (2023.0, 2025.0, "对话与 IDE 阶段", C[2]), (2025.0, 2026.95, "智能体阶段", C[0])]:
    ax.add_patch(Rectangle((a, -0.02), b - a, 0.04, color=c, alpha=0.9, zorder=2))
    ax.text((a + b) / 2, -0.22, t, ha="center", fontsize=8, color=c, weight="bold")
ev_up = [(2021.5, "Copilot 技术预览"), (2022.5, "Copilot GA（$10/月）"), (2022.9, "ChatGPT"), (2023.3, "Cursor 发布"), (2024.25, "Devin"), (2024.5, "Claude 3.5 Sonnet"), (2024.8, "Bolt / Lovable 上线"), (2024.9, "MCP 发布"), (2025.1, "DeepSeek R1；\n\"vibe coding\"一词"), (2025.4, "Claude Code 正式发布"), (2025.55, "Windsurf 分拆"), (2025.8, "Claude Code 周限额"), (2025.95, "Menlo：编程占企业\nAI 支出 55%"), (2026.3, "Copilot 冻结注册；\nCodex 改 token 计费"), (2026.45, "全行业转用量计费"), (2026.62, "SpaceX 收购 Cursor\n（$600 亿）"), (2026.77, "SO 2026：智能体\n成主流")]
for i, (x, t) in enumerate(ev_up):
    lvl = [0.30, 0.58, 0.86][i % 3]
    ax.plot([x, x], [0.04, lvl - 0.05], color="#c8c7c1", lw=0.7, zorder=1)
    ax.plot(x, 0, "o", color="white", mec=C[0], ms=4, zorder=3)
    ax.text(x, lvl, t, ha="center", va="center", fontsize=6.3, color=TXT, bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#dedcd6", lw=0.6))
ev_dn = [(2025.0, "Cursor ARR $1 亿"), (2025.45, "Cursor ARR $5 亿\nLovable ARR $1 亿"), (2025.85, "Cursor ARR $10 亿+\nClaude Code ~$10 亿"), (2026.05, "Copilot 付费 470 万"), (2026.4, "Anthropic run-rate $470 亿\nCursor ARR $30 亿+"), (2026.75, "Cognition 估值 $480 亿\nLovable ARR 预计 $6 亿")]
for i, (x, t) in enumerate(ev_dn):
    lvl = [-0.52, -0.82][i % 2]
    ax.plot([x, x], [-0.04, lvl + 0.08], color="#c8c7c1", lw=0.7, zorder=1)
    ax.plot(x, 0, "o", color="white", mec=C[1], ms=4, zorder=3)
    ax.text(x, lvl, t, ha="center", va="center", fontsize=6.3, color=TXT2, bbox=dict(boxstyle="round,pad=0.25", fc="#fff8f4", ec="#f3c9b5", lw=0.6))
ax.text(2021.25, 0.95, "产品与技术事件", fontsize=7, color=C[0], weight="bold")
ax.text(2021.25, -0.95, "收入与资本事件（公司自述/媒体报道）", fontsize=7, color=C[1], weight="bold")
save(fig, "fig2_1_timeline.png")

# ---------- fig2_2 market size (log) ----------
fig, ax = plt.subplots(figsize=(6.3, 3.0))
labels = ["Precedence\n2025 年", "Global Industry\nAnalysts 2024 年", "Menlo（美国企业\n编程支出）2025 年", "MarketsandMarkets\n2025 年", "Grand View\n2030 年预测", "IDC 中国\n2025 年"]
vals = [0.05025, 0.0259, 4.0, 8.14, 26.03, 0.055]
cols = [C[0], C[0], C[1], C[0], C[0], C[2]]
y = np.arange(len(labels))
ax.barh(y, vals, color=cols, height=0.62)
ax.set_xscale("log"); ax.set_xlim(0.01, 100)
ax.set_yticks(y); ax.set_yticklabels(labels); ax.invert_yaxis()
ax.set_xlabel("十亿美元（对数坐标）")
for yi, v in zip(y, vals):
    ax.text(v * 1.15, yi, f"{v:.3g}" if v < 1 else f"{v:.1f}", va="center", fontsize=8, color=TXT)
ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(length=0)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=C[0], label="厂商收入口径（全球）"), Patch(color=C[1], label="买方支出口径（美国企业）"), Patch(color=C[2], label="厂商收入口径（中国，按 7.2 汇率折算）")], loc="lower right", frameon=False)
ax.text(0.011, 5.75, "同一个\"市场\"，口径不同，数值相差两个数量级", fontsize=7.5, color=TXT2)
save(fig, "fig2_2_marketsize.png")

# ---------- fig2_3 ARR trajectories ----------
fig, ax = plt.subplots(figsize=(6.3, 3.4))
import datetime as dt
def d(s): return dt.date.fromisoformat(s)
series = {
 "Cursor（年化收入）": ([("2025-01-15", 0.1), ("2025-03-15", 0.2), ("2025-06-05", 0.5), ("2025-11-13", 1.0), ("2026-02-15", 2.0), ("2026-05-21", 3.0), ("2026-06-09", 4.0)], C[0]),
 "Claude Code（匿名信源）": ([("2025-10-15", 1.0), ("2026-02-12", 2.5)], C[1]),
 "Cognition（Devin+Windsurf）": ([("2025-07-14", 0.082), ("2026-05-27", 0.492), ("2026-09-08", 0.9)], C[2]),
 "Lovable": ([("2024-12-15", 0.004), ("2025-07-15", 0.1), ("2025-12-01", 0.2), ("2026-02-15", 0.4), ("2026-06-09", 0.5), ("2026-08-31", 0.6)], C[3]),
 "Replit（含 Sacra 估计）": ([("2025-06-15", 0.1), ("2025-12-15", 0.265), ("2026-04-15", 0.525)], C[4]),
}
for name, (pts, c) in series.items():
    xs = [d(a) for a, b in pts]; ys = [b for a, b in pts]
    ax.plot(xs, ys, "-o", color=c, lw=2, ms=4, label=name)
    ax.text(xs[-1], ys[-1], f"  {ys[-1]:.2g}", fontsize=7.5, color=TXT, va="center")
ax.set_ylabel("年化收入（十亿美元）"); ax.set_yscale("log"); ax.set_ylim(0.003, 8)
ax.set_xlim(d("2024-11-15"), d("2026-11-30"))
import matplotlib.dates as mdates
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10])); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
tidy(ax); ax.legend(frameon=False, loc="lower right", ncol=2)
ax.text(d("2024-11-25"), 5.5, "对数坐标；各点为公司自述或媒体报道，未经审计", fontsize=7, color=MUTED)
save(fig, "fig2_3_arr.png")

# ---------- fig2_4 adoption & trust ----------
fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.9))
ax = axes[0]
x = np.arange(3); w = 0.36
use = [76, 84, None]; daily = [None, 47.1, 73]
ax.bar(x[:2] - w/2, [76, 84], w, color=C[0], label="使用或计划使用（全体）")
ax.bar([x[1] + w/2, x[2] + w/2], [47.1, 73], w, color=C[2], label="每日使用（2025：全体；2026：助手/智能体用户）")
for xi, v in zip(x[:2] - w/2, [76, 84]): ax.text(xi, v + 1.5, f"{v}%", ha="center", fontsize=7.5)
for xi, v in zip([x[1] + w/2, x[2] + w/2], [47.1, 73]): ax.text(xi, v + 1.5, f"{v}%", ha="center", fontsize=7.5)
ax.set_xticks(x); ax.set_xticklabels(["SO 2024", "SO 2025", "SO 2026"]); ax.set_ylim(0, 100)
ax.set_title("采用率（Stack Overflow）", fontsize=9); tidy(ax); ax.legend(frameon=False, fontsize=6.3, loc="upper left")
ax = axes[1]
labels = ["SO 2024", "SO 2025", "SO 2026", "DORA 2024", "DORA 2025"]
trust = [40, 29, 48, None, 24]; distrust = [31, 46, None, 39, 30]
xx = np.arange(len(labels))
ax.bar(xx - w/2, [v if v else 0 for v in trust], w, color=C[0], label="信任（SO 2026：\"易验证时\"信任）")
ax.bar(xx + w/2, [v if v else 0 for v in distrust], w, color=C[1], label="不信任 / 信任很少")
for i, v in enumerate(trust):
    if v: ax.text(xx[i] - w/2, v + 1.5, f"{v}%", ha="center", fontsize=7.5)
for i, v in enumerate(distrust):
    if v: ax.text(xx[i] + w/2, v + 1.5, f"{v}%", ha="center", fontsize=7.5)
ax.set_xticks(xx); ax.set_xticklabels(labels, fontsize=7); ax.set_ylim(0, 60)
ax.set_title("对 AI 输出准确性的信任", fontsize=9); tidy(ax); ax.legend(frameon=False, fontsize=6.3, loc="upper left")
ax.text(2.6, 54, "SO 2026 用于重要决策\n时信任仅 6.6%", fontsize=6.5, color=TXT2)
fig.tight_layout()
save(fig, "fig2_4_adoption_trust.png")

# ---------- fig2_5 china ----------
fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.8), gridspec_kw={"width_ratios": [1.15, 1]})
ax = axes[0]
names = ["阿里（Qoder）", "智谱（CodeGeeX）", "商汤（Raccoon）", "腾讯（CodeBuddy）", "百度（Comate）", "其他"]
sh = [47.6, 11.5, 10.5, 6.9, 6.0, 17.5]
y = np.arange(len(names))
ax.barh(y, sh, color=[C[0]] + [C[0]] * 4 + ["#c8c7c1"], height=0.62)
for yi, v in zip(y, sh): ax.text(v + 0.8, yi, f"{v:.1f}%", va="center", fontsize=7.5)
ax.set_yticks(y); ax.set_yticklabels(names, fontsize=7.5); ax.invert_yaxis(); ax.set_xlim(0, 60)
ax.set_title("IDC：2025 年中国 AI 编程市场份额（收入）", fontsize=8.5); ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(length=0)
ax.text(1, 5.6, "\"其他\"为 100% 减前五名所得，研究者计算", fontsize=6, color=MUTED)
ax = axes[1]
labels = ["IDC 2025", "IDC 2026E", "信通院口径\n2025（CSDN 转述）"]
vals = [3.99, 11.73, 47.2]
ax.bar(np.arange(3), vals, color=[C[0], "#8db3e7", C[1]], width=0.6)
for i, v in enumerate(vals): ax.text(i, v + 1, f"{v} 亿元", ha="center", fontsize=7.5)
ax.set_xticks(np.arange(3)); ax.set_xticklabels(labels, fontsize=7); ax.set_ylim(0, 56)
ax.set_title("两种口径的市场规模（人民币，亿元）", fontsize=8.5); tidy(ax)
ax.text(1.3, 30, "相差约 12 倍：\n口径不同，不可互换", fontsize=7, color=TXT2, ha="center")
fig.tight_layout()
save(fig, "fig2_5_china.png")

# ---------- fig3_1 PEST matrix ----------
fig, ax = blank(6.3, 4.5)
quad = [
 ("P 政治与政策", C[0], ["欧盟 AI Act：GPAI 义务 2025-08 生效，高风险推迟至 2027-12 → 门槛（落在模型方）", "中国：备案/登记（累计 988 款）、内容标识（2025-09）→ 门槛；\"人工智能+\"与开源支持 → 供给", "美国 AI Action Plan：推动开放权重、去监管 → 供给/成本", "芯片出口管制 → 中国模型转向效率与低价 → 竞争", "Doe v. GitHub：DMCA 诉求被驳回（2026-09）→ 门槛下降；可版权性取决于人类投入 → 需求（审阅记录）"]),
 ("E 经济", C[1], ["推理成本年均下降约 10 倍；开源比闭源便宜 80–95% → 成本/竞争（模型商品化）", "企业编程 AI 支出 $40 亿、占 55%；38% 组织设用量上限 → 需求/成本治理", "初级岗位收缩（22–25 岁 −13%）、资深稳定 → 需求结构（独立开发者扩大）", "头部融资与并购数百亿美元 → 进入门槛（通用赛道）"]),
 ("S 社会", C[2], ["DORA：AI 是放大器，吞吐↑但不稳定性↑ → 需求（验证/流程）", "Claude Code 79% 自动化使用；每日数小时 → 需求（上下文、成本控制）", "非技术构建者 80%（Lovable 自报）；Gartner：2028 年 60% vibe-coded 应用被弃用 → 需求转向治理与维护", "信任下降（46% 不信任）；安全事故（CVE-2025-48757、Replit 删库）→ 门槛（安全默认值）"]),
 ("T 技术", C[6], ["SWE-bench Verified 33% → 95%；Pro 仅 ~78% → 供给（可委托任务扩大）", "1M 上下文、压缩、子智能体；但 context rot → 供给/竞争（上下文工程成护城河）", "MCP 中立托管，10,000+ 服务器 → 集成成本下降 → 门槛下降", "开源模型（DeepSeek、Qwen、GLM、Kimi）MIT/Apache → 成本/门槛下降"]),
]
pos = [(0.0, 0.5), (0.5, 0.5), (0.0, 0.0), (0.5, 0.0)]
for (title, c, items), (x0, y0) in zip(quad, pos):
    ax.add_patch(Rectangle((x0 + 0.005, y0 + 0.005), 0.49, 0.49, fc="white", ec=c, lw=1.2))
    ax.add_patch(Rectangle((x0 + 0.005, y0 + 0.425), 0.49, 0.07, fc=c, ec=c))
    ax.text(x0 + 0.02, y0 + 0.46, title, fontsize=9, color="white", weight="bold", va="center")
    yy = y0 + 0.395
    for it in items:
        ax.text(x0 + 0.02, yy, "• " + it, fontsize=6.1, va="top", color=TXT, wrap=True, linespacing=1.2)
        lines = max(1, int(len(it) * 6.1 * 0.0105 / 0.47) + 1)
        yy -= 0.03 * lines + 0.012
save(fig, "fig3_1_pest.png")

# ---------- fig3_2 price spectrum ----------
fig, axes = plt.subplots(1, 2, figsize=(6.3, 3.0), gridspec_kw={"width_ratios": [1.4, 1]})
ax = axes[0]
models = ["Claude Fable 5.1", "gpt-6-astra", "Claude Opus 5.5", "Kimi K3", "Claude Sonnet 5.5", "gpt-6.1-sol", "Gemini 3.1 Pro", "gpt-5.3-codex", "DeepSeek V4-Pro", "Gemini 3.8 Flash", "Kimi K2.5 (Bedrock)", "Qwen3 Coder Next (Bedrock)", "Cursor Composer 2.5", "DeepSeek V4.1-Flash", "Claude Haiku 5.5", "gpt-6-luna"]
price = [10, 10, 4, 3.0, 2, 2, 2, 1.75, 1.32, 0.75, 0.60, 0.50, 0.50, 0.30, 0.10, 0.10]
kind = ["闭源"] * 3 + ["开源/国产"] + ["闭源"] * 4 + ["开源/国产"] + ["闭源"] + ["开源/国产"] * 2 + ["工具自研"] + ["开源/国产"] + ["闭源"] * 2
cm = {"闭源": C[0], "开源/国产": C[1], "工具自研": C[2]}
y = np.arange(len(models))
ax.barh(y, price, color=[cm[k] for k in kind], height=0.65)
ax.set_xscale("log"); ax.set_xlim(0.05, 25); ax.set_xticks([0.1, 1, 10]); ax.set_xticklabels(["0.1", "1", "10"]); ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_yticks(y); ax.set_yticklabels(models, fontsize=6.5); ax.invert_yaxis()
for yi, v in zip(y, price): ax.text(v * 1.12, yi, f"${v:g}", va="center", fontsize=6.5)
ax.set_xlabel("输入价格，美元/百万 token（对数）", fontsize=7.5); ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(length=0)
ax.legend(handles=[Patch(color=cm[k], label=k) for k in cm], frameon=False, fontsize=6.5, loc="lower right")
ax.set_title("2026-10 编程模型 API 输入价格谱", fontsize=8.5)
ax = axes[1]
gens = ["Opus 4 / 4.1\n(2025)", "Opus 4.5–5\n(2025-11~)", "Opus 5.5\n(2026)"]
inp = [15, 5, 4]; outp = [75, 25, 20]
xx = np.arange(3); w = 0.36
ax.bar(xx - w/2, inp, w, color=C[0], label="输入")
ax.bar(xx + w/2, outp, w, color="#8db3e7", label="输出")
for i in range(3):
    ax.text(xx[i] - w/2, inp[i] + 1.5, f"${inp[i]}", ha="center", fontsize=7); ax.text(xx[i] + w/2, outp[i] + 1.5, f"${outp[i]}", ha="center", fontsize=7)
ax.set_xticks(xx); ax.set_xticklabels(gens, fontsize=7); ax.set_ylim(0, 90)
ax.set_title("Anthropic 旗舰档定价变化", fontsize=8.5); tidy(ax); ax.legend(frameon=False, fontsize=7)
ax.text(1, 82, "同档价格约两年内下降 3–4 倍", ha="center", fontsize=7, color=TXT2)
fig.tight_layout()
save(fig, "fig3_2_prices.png")

# ---------- fig3_3 SWE-bench ----------
fig, ax = plt.subplots(figsize=(6.3, 3.1))
pts = [("2024-06", 33.4, "Claude 3.5 Sonnet"), ("2024-08", 33.2, "GPT-4o"), ("2024-10", 49.0, "Claude 3.5 Sonnet(新)"), ("2025-02", 62.3, "Claude 3.7 Sonnet"), ("2025-09", 77.2, "Claude Sonnet 4.5"), ("2025-11", 80.9, "Claude Opus 4.5"), ("2026-02", 80.8, "Claude Opus 4.6"), ("2026-04", 88.7, "GPT-5.5"), ("2026-05", 88.6, "Claude Opus 4.8"), ("2026-06", 95.0, "Claude Fable 5")]
xs = [d(p[0] + "-15") for p in pts]; ys = [p[1] for p in pts]
ax.plot(xs, ys, "-", color=C[0], lw=2, label="SWE-bench Verified 顶分（厂商自报）")
ax.plot(xs, ys, "o", color=C[0], ms=4)
for x, y_, t in zip(xs, ys, [p[2] for p in pts]):
    ax.annotate(t, (x, y_), xytext=(0, 7 if t not in ("GPT-4o", "Claude Opus 4.6") else -11), textcoords="offset points", ha="center", fontsize=6, color=TXT2)
pro = [("2025-09", 23.3, "GPT-5"), ("2026-05", 77.8, "Claude Mythos Preview（公开集）"), ("2025-09", 17.8, "Opus 4.1（商业私有集）")]
ax.plot([d("2025-09-15"), d("2026-05-15")], [23.3, 77.8], "-s", color=C[1], lw=2, ms=4, label="SWE-bench Pro 公开集顶分")
ax.plot([d("2025-09-15")], [17.8], "D", color=C[7], ms=5, label="SWE-bench Pro 商业私有集（Opus 4.1）")
ax.annotate("GPT-5 23.3%", (d("2025-09-15"), 23.3), xytext=(6, -2), textcoords="offset points", fontsize=6, color=TXT2)
ax.annotate("17.8%", (d("2025-09-15"), 17.8), xytext=(6, -8), textcoords="offset points", fontsize=6, color=TXT2)
ax.annotate("77.8%", (d("2026-05-15"), 77.8), xytext=(5, -9), textcoords="offset points", fontsize=6, color=TXT2)
ax.set_ylim(0, 105); ax.set_ylabel("通过率（%）")
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7])); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
tidy(ax); ax.legend(frameon=False, fontsize=6.5, loc="lower right")
save(fig, "fig3_3_swebench.png")
