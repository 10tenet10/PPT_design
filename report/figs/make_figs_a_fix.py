from common import *
import datetime as dt, textwrap
import matplotlib.dates as mdates
from matplotlib.patches import Patch
def d(s): return dt.date.fromisoformat(s)

import re as _re
def _units(s):
    return sum(1.0 if ord(ch) > 0x2E80 else 0.62 for ch in s)
NO_START = set("，。、；：？！）》」』】〕%％·…—～")
NO_END = set("（《「『【〔")
def wrap_cjk(text, units):
    """wrap by display width; CJK chars break anywhere, latin words and number+unit kept whole;
    kinsoku: closing punctuation never starts a line, opening punctuation never ends one; keeps explicit newlines"""
    units *= 0.88
    out = []
    for para in text.split("\n"):
        tokens = _re.findall(r"[$~≈<>]?\d[\d,\.]*(?:\s?[–\-~]\s?\d[\d,\.]*)?\s?(?:亿|万|倍|%|个|年|月|日|天|小时|条|款|家|位|人)?\+?|[A-Za-z0-9$%~\-\.,/+:\'\"]+ ?|.", para)
        lines = []; cur = ""; w = 0.0
        for tk in tokens:
            u = _units(tk)
            if w + u > units and cur and tk[0] not in NO_START:
                carry = ""
                while cur and cur[-1] in NO_END:
                    carry = cur[-1] + carry; cur = cur[:-1]
                lines.append(cur.rstrip()); cur = carry + tk.lstrip(); w = _units(cur)
            else:
                cur += tk; w += u
        if cur: lines.append(cur.rstrip())
        out.extend(lines if lines else [""])
    return "\n".join(out), len(out)

# ---------- fig1_1 boundary (fixed v3: titles inside frames, wider gaps) ----------
fig, ax = blank(6.3, 4.1)
box(ax, 0.27, 0.30, 0.46, 0.40, "", fc="#e9f1fc", ec=C[0], lw=1.4, rounding=0.03)
ax.text(0.50, 0.655, "AI 编程工具行业（本报告范围）", ha="center", fontsize=9, weight="bold", color=C[0])
items = ["IDE 内嵌\n助手", "AI 原生\nIDE", "终端/CLI\n智能体", "云端异步\n智能体", "一体化\n应用平台"]
xs = [0.29, 0.375, 0.46, 0.545, 0.63]
for x, t in zip(xs, items):
    box(ax, x, 0.35, 0.078, 0.22, t, fc="white", ec=C[0], fs=6.4)
box(ax, 0.02, 0.765, 0.96, 0.215, "", fc=LIGHT, ec="#c8c7c1", rounding=0.02)
ax.text(0.5, 0.948, "上游投入（产业链分析，不计入市场规模）", ha="center", va="center", fontsize=8, color=TXT2)
for x, t in zip([0.04, 0.36, 0.68], ["基础模型\nAnthropic、OpenAI、Google、\nDeepSeek、Qwen、Kimi、GLM", "算力与云\nNVIDIA、AWS、Azure、GCP、\n阿里云、火山引擎", "模型厂商自营编程产品\nClaude Code、Codex、\nGemini Code Assist"]):
    box(ax, x, 0.78, 0.28, 0.135, t, fc="white", ec="#c8c7c1", fs=6.2)
arrow(ax, 0.5, 0.765, 0.5, 0.705, color="#8a8984")
ax.text(0.512, 0.735, "模型厂商自营产品计入行业", fontsize=6.3, color=TXT2, ha="left", va="center")
box(ax, 0.02, 0.30, 0.18, 0.40, "传统开发工具\n（运行基础，\n配套环节）\n\nGit / GitHub\nCI/CD、测试框架\n可观测性、IDE", fc=LIGHT, ec="#c8c7c1", fs=6.6)
arrow(ax, 0.20, 0.50, 0.27, 0.50, color="#8a8984", style="<|-|>")
box(ax, 0.80, 0.30, 0.18, 0.40, "替代品\n\n低代码 / 无代码平台\n直接使用 ChatGPT /\nClaude 聊天\n外包与自由职业者", fc="#fdf1ec", ec=C[1], fs=6.6)
arrow(ax, 0.73, 0.50, 0.80, 0.50, color=C[1], style="<|-|>", ls="--")
ax.text(0.765, 0.545, "融合中", ha="center", va="center", fontsize=5.8, color=C[1])
box(ax, 0.02, 0.02, 0.96, 0.215, "", fc=LIGHT, ec="#c8c7c1", rounding=0.02)
ax.text(0.5, 0.205, "下游用户", ha="center", va="center", fontsize=8, color=TXT2)
for x, t, fc in zip([0.06, 0.30, 0.54, 0.78], ["企业研发团队", "专业独立开发者", "创业团队", "低编程基础用户\n（本报告重点细分）"], ["white", "white", "white", "#fff3d6"]):
    box(ax, x, 0.045, 0.20, 0.11, t, fc=fc, ec="#c8c7c1" if fc == "white" else C[3], fs=6.5)
arrow(ax, 0.5, 0.30, 0.5, 0.24, color="#8a8984")
save(fig, "fig1_1_boundary.png")

# ---------- fig2_1 timeline redesign: year columns ----------
TH = 4.6; LS = 0.027 * 4.4 / TH
fig, ax = blank(6.3, TH)
years = ["2021", "2022", "2023", "2024", "2025", "2026（至 10 月）"]
widths = [0.12, 0.125, 0.125, 0.17, 0.235, 0.225]
bounds = [0]
for w_ in widths: bounds.append(bounds[-1] + w_)
phase = [("补全阶段", 0, 2, C[3]), ("对话与 IDE 阶段", 2, 4, C[2]), ("智能体阶段", 4, 6, C[0])]
for name, a, b, c in phase:
    ax.add_patch(Rectangle((bounds[a] + 0.004, 0.93), bounds[b] - bounds[a] - 0.008, 0.06, fc=c, ec=c))
    ax.text((bounds[a] + bounds[b]) / 2, 0.96, name, ha="center", va="center", fontsize=8, color="white", weight="bold")
tech = [
 ["6 月 Copilot 技术预览"],
 ["6 月 Copilot GA，$10/月", "11 月 ChatGPT 发布"],
 ["3 月 Cursor 发布", "Gartner：企业工程师使用率<10%"],
 ["3 月 Devin 发布", "6 月 Claude 3.5 Sonnet", "10–11 月 Bolt.new、Lovable 上线", "11 月 MCP 发布"],
 ["1 月 DeepSeek R1", "2 月 \"vibe coding\"一词；Claude Code 预览", "5 月 Claude Code 正式发布", "6 月 Anthropic 限供 Windsurf", "7 月 Windsurf 分拆；Replit 删库事件", "8 月 Claude Code 周限额", "12 月 MCP 入 AAIF；Menlo：编程占 55%"],
 ["2 月 Claude Code 2.0；Codex 桌面版", "3 月 Composer 2（Kimi 基座）", "4 月 Copilot 冻结注册；Codex 改 token 计费", "6 月 全行业转用量计费；Gemini CLI 收回个人版", "8 月 SpaceX 完成收购 Cursor；OpenAI 对 Cursor 断供", "10 月 SO 2026：智能体成主流"],
]
money = [
 [], [], ["Cursor 种子轮 $800 万"], ["11 月 Cursor 收购 Supermaven"],
 ["1 月 Cursor ARR $1 亿", "6 月 Cursor ARR $5 亿、估值 $99 亿", "7 月 Lovable ARR $1 亿；Copilot 用户 2,000 万", "11 月 Cursor ARR $10 亿+；Claude Code ~$10 亿"],
 ["1 月 Copilot 付费订阅 470 万", "5 月 Anthropic run-rate $470 亿；Cursor ARR $30 亿", "8 月 Lovable 估值 $133 亿；SpaceX 收购 Cursor $600 亿", "9 月 Cognition 估值 $480 亿、ARR ~$9 亿"],
]
ax.add_patch(Rectangle((0, 0.40), 1, 0.50, fc="white", ec="#dedcd6", lw=0.8))
ax.add_patch(Rectangle((0, 0.0), 1, 0.38, fc="#fff8f4", ec="#f3c9b5", lw=0.8))
ax.text(0.005, 0.893, "产品与技术事件", fontsize=6.5, color=C[0], weight="bold", va="top")
ax.text(0.005, 0.375, "收入与资本事件（公司自述/媒体报道）", fontsize=6.5, color=C[1], weight="bold", va="top")
for i, y in enumerate(years):
    x0 = bounds[i]; cw = widths[i]
    if i > 0:
        ax.plot([x0, x0], [0.0, 0.90], color="#dedcd6", lw=0.6)
    ax.text(x0 + cw / 2, 0.855, y, ha="center", va="top", fontsize=7.5, weight="bold", color=TXT)
    units = cw * 6.3 * 72 / 5.5 * 0.80
    yy = 0.81
    for ev in tech[i]:
        t, n = wrap_cjk(ev, units)
        ax.text(x0 + 0.006, yy, "• " + t, fontsize=5.5, va="top", color=TXT, linespacing=1.15)
        yy -= LS * n + 0.011
    yy = 0.335
    for ev in money[i]:
        t, n = wrap_cjk(ev, units)
        ax.text(x0 + 0.006, yy, "• " + t, fontsize=5.5, va="top", color=TXT2, linespacing=1.15)
        yy -= LS * n + 0.011
save(fig, "fig2_1_timeline.png")

# ---------- fig2_2 market size legend fix ----------
fig, ax = plt.subplots(figsize=(6.3, 3.1))
labels = ["Precedence\n2025 年", "Global Industry\nAnalysts 2024 年", "Menlo（美国企业\n编程支出）2025 年", "MarketsandMarkets\n2025 年", "Grand View\n2030 年预测", "IDC 中国\n2025 年"]
vals = [0.05025, 0.0259, 4.0, 8.14, 26.03, 0.055]
cols = [C[0], C[0], C[1], C[0], C[0], C[2]]
y = np.arange(len(labels))
ax.barh(y, vals, color=cols, height=0.62)
ax.set_xscale("log"); ax.set_xlim(0.01, 100)
ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=7.5); ax.invert_yaxis()
ax.set_xlabel("十亿美元（对数坐标）")
for yi, v in zip(y, vals):
    ax.text(v * 1.15, yi, f"{v:.3g}" if v < 1 else f"{v:.1f}", va="center", fontsize=8, color=TXT)
ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(length=0)
ax.legend(handles=[Patch(color=C[0], label="厂商收入口径（全球）"), Patch(color=C[1], label="买方支出口径（美国企业）"), Patch(color=C[2], label="厂商收入口径（中国，按 7.2 汇率折算）")], loc="lower left", bbox_to_anchor=(0, 1.0), ncol=3, frameon=False, fontsize=6.8)
save(fig, "fig2_2_marketsize.png")

# ---------- fig2_4 adoption/trust legend fix ----------
fig, axes = plt.subplots(1, 2, figsize=(6.3, 3.1))
ax = axes[0]; w = 0.36; x = np.arange(3)
ax.bar(x[:2] - w/2, [76, 84], w, color=C[0], label="使用或计划使用（全体受访者）")
ax.bar([x[1] + w/2, x[2]], [47.1, 73], w, color=C[2], label="每日使用（2025：全体；2026：助手/智能体用户）")
for xi, v in zip(x[:2] - w/2, [76, 84]): ax.text(xi, v + 1.5, f"{v}%", ha="center", fontsize=7.5)
for xi, v in zip([x[1] + w/2, x[2]], [47.1, 73]): ax.text(xi, v + 1.5, f"{v}%", ha="center", fontsize=7.5)
ax.set_xticks(x); ax.set_xticklabels(["SO 2024", "SO 2025", "SO 2026"]); ax.set_ylim(0, 100)
ax.set_title("采用率（Stack Overflow）", fontsize=9); tidy(ax)
ax.legend(frameon=False, fontsize=6.2, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=1)
ax = axes[1]
labels = ["SO 2024", "SO 2025", "SO 2026", "DORA 2024", "DORA 2025"]
trust = [40, 29, 48, None, 24]; distrust = [31, 46, None, 39, 30]
xx = np.arange(len(labels))
ax.bar(xx - w/2, [v if v else 0 for v in trust], w, color=C[0], label="信任（SO 2026 为\"易验证时\"信任；重要决策时仅 6.6%）")
ax.bar(xx + w/2, [v if v else 0 for v in distrust], w, color=C[1], label="不信任 / 信任很少")
for i, v in enumerate(trust):
    if v: ax.text(xx[i] - w/2, v + 1.2, f"{v}%", ha="center", fontsize=7.5)
for i, v in enumerate(distrust):
    if v: ax.text(xx[i] + w/2, v + 1.2, f"{v}%", ha="center", fontsize=7.5)
ax.set_xticks(xx); ax.set_xticklabels(labels, fontsize=7); ax.set_ylim(0, 60)
ax.set_title("对 AI 输出准确性的信任", fontsize=9); tidy(ax)
ax.legend(frameon=False, fontsize=6.2, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=1)
fig.tight_layout()
save(fig, "fig2_4_adoption_trust.png")

# ---------- fig3_1 PEST matrix (manual wrap) ----------
H = 3.75; K = 4.3 / H
fig, ax = blank(6.3, H)
quad = [
 ("P 政治与政策", C[0], ["欧盟 AI Act：GPAI 义务 2025-08 生效，高风险义务推迟至 2027-12 → 门槛（主要落在模型方）", "中国：备案/登记（累计 988 款）、内容标识（2025-09）→ 门槛；\"人工智能+\"与开源支持 → 供给", "美国 AI Action Plan：推动开放权重、去监管 → 供给/成本", "芯片出口管制 → 中国模型转向效率与低价 → 竞争", "Doe v. GitHub：DMCA 诉求被驳回（2026-09）→ 门槛下降；可版权性取决于人类投入 → 需求（审阅记录）"]),
 ("E 经济", C[1], ["推理成本年均下降约 10 倍；开源比闭源便宜 80–95% → 成本/竞争（模型商品化）", "企业编程 AI 支出 $40 亿、占 55%；38% 组织设用量上限 → 需求/成本治理", "初级岗位收缩（22–25 岁 −13%）、资深稳定 → 需求结构（独立开发者扩大）", "头部融资与并购达数百亿美元 → 进入门槛（通用赛道）"]),
 ("S 社会", C[2], ["DORA：AI 是放大器，吞吐↑但不稳定性↑ → 需求（验证/流程）", "Claude Code 79% 为自动化使用；每日数小时 → 需求（上下文、成本控制）", "非技术构建者 80%（Lovable 自报）；Gartner：2028 年 60% vibe-coded 应用被弃用 → 需求转向治理与维护", "信任下降（46% 不信任）；安全事故（CVE-2025-48757、Replit 删库）→ 门槛（安全默认值）"]),
 ("T 技术", C[6], ["SWE-bench Verified 33% → 95%；Pro 仅 ~78% → 供给（可委托任务扩大）", "1M 上下文、压缩、子智能体；但 context rot → 供给/竞争（上下文工程成护城河）", "MCP 中立托管，10,000+ 服务器 → 集成成本下降 → 门槛下降", "开源模型（DeepSeek、Qwen、GLM、Kimi）MIT/Apache → 成本/门槛下降"]),
]
pos = [(0.0, 0.5), (0.5, 0.5), (0.0, 0.0), (0.5, 0.0)]
for (title, c, items), (x0, y0) in zip(quad, pos):
    ax.add_patch(Rectangle((x0 + 0.005, y0 + 0.005), 0.49, 0.49, fc="white", ec=c, lw=1.2))
    ax.add_patch(Rectangle((x0 + 0.005, y0 + 0.495 - 0.065 * K), 0.49, 0.065 * K, fc=c, ec=c))
    ax.text(x0 + 0.02, y0 + 0.495 - 0.0325 * K, title, fontsize=9, color="white", weight="bold", va="center")
    yy = y0 + 0.495 - 0.065 * K - 0.025 * K
    for it in items:
        t, n = wrap_cjk(it, 29)
        ax.text(x0 + 0.02, yy, "• " + t, fontsize=6.2, va="top", color=TXT, linespacing=1.2)
        yy -= (0.0285 * n + 0.012) * K
save(fig, "fig3_1_pest.png")

# ---------- fig3_3 SWE-bench (label fix) ----------
fig, ax = plt.subplots(figsize=(6.3, 3.2))
pts = [("2024-06", 33.4, "Claude 3.5 Sonnet", (0, 8)), ("2024-08", 33.2, "GPT-4o", (0, -11)), ("2024-10", 49.0, "Claude 3.5 Sonnet(新)", (0, 8)), ("2025-02", 62.3, "Claude 3.7 Sonnet", (0, 8)), ("2025-09", 77.2, "Claude Sonnet 4.5", (-6, 8)), ("2025-11", 80.9, "Claude Opus 4.5", (4, 8)), ("2026-02", 80.8, "Claude Opus 4.6", (0, -11)), ("2026-04", 88.7, "GPT-5.5", (-14, 6)), ("2026-05", 88.6, "Claude Opus 4.8", (10, -11)), ("2026-06", 95.0, "Claude Fable 5", (0, 7))]
xs = [d(p[0] + "-15") for p in pts]; ys = [p[1] for p in pts]
ax.plot(xs, ys, "-", color=C[0], lw=2, label="SWE-bench Verified 顶分（厂商自报）")
ax.plot(xs, ys, "o", color=C[0], ms=4)
for x, y_, t, off in zip(xs, ys, [p[2] for p in pts], [p[3] for p in pts]):
    ax.annotate(t, (x, y_), xytext=off, textcoords="offset points", ha="center", fontsize=6, color=TXT2)
ax.plot([d("2025-09-15"), d("2026-05-15")], [23.3, 77.8], "-s", color=C[1], lw=2, ms=4, label="SWE-bench Pro 公开集顶分")
ax.plot([d("2025-09-15")], [17.8], "D", color=C[7], ms=5, label="SWE-bench Pro 商业私有集（Opus 4.1）")
ax.annotate("GPT-5 23.3%", (d("2025-09-15"), 23.3), xytext=(6, 2), textcoords="offset points", fontsize=6, color=TXT2)
ax.annotate("Opus 4.1 17.8%", (d("2025-09-15"), 17.8), xytext=(6, -9), textcoords="offset points", fontsize=6, color=TXT2)
ax.annotate("Mythos Preview 77.8%", (d("2026-05-15"), 77.8), xytext=(2, -11), textcoords="offset points", fontsize=6, color=TXT2, ha="center")
ax.set_ylim(0, 108); ax.set_ylabel("通过率（%）")
ax.set_xlim(d("2024-04-01"), d("2026-09-01"))
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7])); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
tidy(ax); ax.legend(frameon=False, fontsize=6.5, loc="upper left")
save(fig, "fig3_3_swebench.png")

# china note shift
fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.8), gridspec_kw={"width_ratios": [1.15, 1]})
ax = axes[0]
names = ["阿里（Qoder）", "智谱（CodeGeeX）", "商汤（Raccoon）", "腾讯（CodeBuddy）", "百度（Comate）", "其他"]
sh = [47.6, 11.5, 10.5, 6.9, 6.0, 17.5]
y = np.arange(len(names))
ax.barh(y, sh, color=[C[0]] * 5 + ["#c8c7c1"], height=0.62)
for yi, v in zip(y, sh): ax.text(v + 0.8, yi, f"{v:.1f}%", va="center", fontsize=7.5)
ax.set_yticks(y); ax.set_yticklabels(names, fontsize=7.5); ax.invert_yaxis(); ax.set_xlim(0, 62)
ax.set_title("IDC：2025 年中国 AI 编程市场份额（收入）", fontsize=8.5); ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(length=0)
ax.text(61, 4.6, "\"其他\"为 100% 减前五名\n所得，研究者计算", fontsize=6.3, color=TXT2, va="center", ha="right", linespacing=1.3)
ax = axes[1]
labels = ["IDC 2025", "IDC 2026E", "信通院口径\n2025（CSDN 转述）"]
vals = [3.99, 11.73, 47.2]
ax.bar(np.arange(3), vals, color=[C[0], "#8db3e7", C[1]], width=0.6)
for i, v in enumerate(vals): ax.text(i, v + 1, f"{v} 亿元", ha="center", fontsize=7.5)
ax.set_xticks(np.arange(3)); ax.set_xticklabels(labels, fontsize=7); ax.set_ylim(0, 56)
ax.set_title("两种口径的市场规模（人民币，亿元）", fontsize=8.5); tidy(ax)
ax.text(0.9, 34, "相差约 12 倍：\n口径不同，不可互换", fontsize=7, color=TXT2, ha="center")
fig.tight_layout()
save(fig, "fig2_5_china.png")
