from common import *
import datetime as dt
import matplotlib.dates as mdates
from matplotlib.patches import Patch, Circle, Polygon
import sys
sys.path.insert(0, "/home/claude/report/figs")
from make_figs_a_fix import wrap_cjk  # noqa (re-runs that file, harmless)

def d(s): return dt.date.fromisoformat(s)

# ---------- fig4_1 industry chain ----------
fig, ax = blank(6.3, 4.5)
LY = {"up": (0.70, 0.27), "mid": (0.37, 0.24), "down": (0.105, 0.14)}
for key, title, c in [("up", "上游：基础模型 · 算力 · 云服务", C[0]), ("mid", "中游：AI 编程工具与平台", C[2]), ("down", "下游：用户", C[3])]:
    y, h = LY[key]
    ax.add_patch(Rectangle((0.0, y), 1.0, h, fc="white", ec="#dedcd6", lw=0.8))
    ax.text(0.008, y + h - 0.01, title, fontsize=7.2, weight="bold", color=c, va="top", zorder=6, bbox=dict(fc="white", ec="none", pad=1.2))
ups = [("Anthropic\nClaude 系列", 0.02), ("OpenAI\nGPT-6 / Codex 模型", 0.215), ("Google\nGemini", 0.41), ("开源/国产模型\nDeepSeek、Qwen、\nKimi、GLM", 0.605), ("算力与云\nNVIDIA、AWS、Azure、\nGCP、阿里云等", 0.80)]
for t, x in ups:
    box(ax, x, 0.735, 0.18, 0.15, t, fc="#e9f1fc", ec=C[0], fs=6.0)
mids = [("模型厂商自营\nClaude Code、Codex、\nAntigravity", 0.02, "#fff3d6", C[3]), ("IDE 内嵌 / AI 原生 IDE\nCopilot、Cursor、Trae、\nKiro、Qoder", 0.215, "white", C[2]), ("云端异步智能体\nDevin、Jules、\nCopilot cloud agent", 0.41, "white", C[2]), ("一体化平台\nLovable、Replit、Bolt、\nv0、Base44", 0.605, "white", C[2]), ("配套服务\nGitHub、Supabase、\nVercel、Netlify", 0.80, LIGHT, "#9a9a94")]
for t, x, fc, ec in mids:
    box(ax, x, 0.395, 0.18, 0.15, t, fc=fc, ec=ec, fs=5.8)
downs = [("企业研发团队\n收入主体（Cursor 75%、\nClaude Code 过半）", 0.02, 0.23), ("专业独立开发者", 0.28, 0.18), ("创业团队", 0.49, 0.18), ("低编程基础用户\n用户数主体，收入少数", 0.72, 0.26)]
for t, x, w_ in downs:
    box(ax, x, 0.112, w_, 0.09, t, fc="white", ec=C[3], fs=5.8)
def a(x1, y1, x2, y2, c="#6f6e69", ls="-", lw=0.9):
    arrow(ax, x1, y1, x2, y2, color=c, ls=ls, lw=lw, mutation=7)
# model -> mid
a(0.11, 0.735, 0.11, 0.545, C[0]); a(0.305, 0.735, 0.15, 0.545, C[0]); a(0.50, 0.735, 0.19, 0.545, C[0])
a(0.11, 0.735, 0.28, 0.545, C[0]); a(0.305, 0.735, 0.31, 0.545, C[7], ls="--"); a(0.50, 0.735, 0.34, 0.545, C[0])
a(0.695, 0.735, 0.37, 0.545, C[1]); a(0.11, 0.735, 0.50, 0.545, C[0]); a(0.11, 0.735, 0.66, 0.545, C[0]); a(0.695, 0.735, 0.72, 0.545, C[1])
a(0.89, 0.735, 0.89, 0.545, "#9a9a94"); a(0.89, 0.735, 0.17, 0.54, "#9a9a94", ls=":")
for x, xd in [(0.11, 0.13), (0.305, 0.37), (0.50, 0.58), (0.695, 0.85)]:
    a(x, 0.395, xd, 0.202, "#8a8984")
a(0.89, 0.395, 0.62, 0.202, "#8a8984")
# legend-like notes
ax.add_patch(Rectangle((0.0, 0.0), 1.0, 0.092, fc=LIGHT, ec="#dedcd6", lw=0.6))
ax.plot([0.015, 0.045], [0.072, 0.072], color=C[7], ls="--", lw=1.2); ax.text(0.05, 0.072, "供给中断：2025-06 Anthropic 限供 Windsurf；2026-11 OpenAI 停止向 Cursor 供模型", fontsize=5.6, va="center")
ax.plot([0.015, 0.045], [0.047, 0.047], color=C[1], lw=1.2); ax.text(0.05, 0.047, "开源基座自研模型：Cursor Composer 2 ← Kimi K2.5；Base44 Base 1", fontsize=5.6, va="center")
ax.plot([0.015, 0.045], [0.022, 0.022], color="#9a9a94", ls=":", lw=1.2); ax.text(0.05, 0.022, "云厂商账单通道：Bedrock / Vertex / Foundry 计费 Claude Code", fontsize=5.6, va="center")
ax.text(0.99, 0.072, "平台持有：Cursor → SpaceX（2026-08）", fontsize=5.6, va="center", ha="right", color=TXT2)
ax.text(0.99, 0.047, "Windsurf → Cognition / Google（2025-07）", fontsize=5.6, va="center", ha="right", color=TXT2)
ax.text(0.99, 0.022, "Base44 → Wix（2025-06）", fontsize=5.6, va="center", ha="right", color=TXT2)
ax.text(0.5, 0.33, "交付接口：GitHub 分支/PR · MCP · Supabase 等 BaaS · 平台一键发布", fontsize=6.0, color=TXT2, ha="center")
save(fig, "fig4_1_chain.png")

# ---------- fig4_2 value flow ----------
fig, axes = plt.subplots(1, 2, figsize=(6.3, 3.2), gridspec_kw={"width_ratios": [1.0, 1.1]})
ax = axes[0]
cats = ["Cursor 2025 年中\n（投资机构估计）", "Replit 2025\n（Sacra 估计区间）", "一体化平台\n托管业务"]
ax.set_xlim(-0.6, 2.6)
bw = 0.72
ax.bar(0, 130, color=C[1], width=bw); ax.bar(0, -30, bottom=0, color=C[7], width=bw)
ax.text(0, 66, "付给模型厂商\n≈130% 收入", ha="center", va="center", fontsize=6.2, color="white")
ax.text(0, -16, "毛利 −30%", ha="center", va="center", fontsize=6.2, color="white")
ax.bar(1, 64, color=C[1], width=bw); ax.bar(1, 36, bottom=64, color=C[2], width=bw)
ax.text(1, 32, "模型接入成本", ha="center", va="center", fontsize=6.2, color="white"); ax.text(1, 82, "毛利 36%\n（高点）", ha="center", va="center", fontsize=6.2, color="white")
ax.text(1, -16, "低点 −14%", ha="center", va="center", fontsize=6.2, color=C[7])
ax.bar(2, 20, color="#c8c7c1", width=bw); ax.bar(2, 80, bottom=20, color=C[2], width=bw)
ax.text(2, 10, "成本", ha="center", va="center", fontsize=6.2, color=TXT); ax.text(2, 60, "毛利 80%+", ha="center", va="center", fontsize=6.2, color="white")
ax.set_xticks([0, 1, 2]); ax.set_xticklabels(cats, fontsize=6.5); ax.set_ylabel("占收入比例（%）"); ax.set_ylim(-40, 140)
ax.axhline(0, color="#9a9a94", lw=0.8); tidy(ax)
ax.set_title("应用层：收入去向与毛利（第三方估计）", fontsize=8)
ax = axes[1]
labels = ["Anthropic 2024", "Anthropic 2025E", "Anthropic 推理业务 2026\n（SemiAnalysis 估计）", "Anthropic 消费者订阅\n（SemiAnalysis 估计）", "OpenAI 计算毛利 2025-10", "Base44 2026 初", "Base44 2026H2\n（自研模型后指引）", "Cursor 2027E\n（自研模型后预测）"]
vals = [-94, 40, 80, 50, 70, 2, 60, 85]
cols = [C[7] if v < 0 else (C[0] if ("Anthropic" in l or "OpenAI" in l) else C[2]) for v, l in zip(vals, labels)]
y = np.arange(len(labels))
ax.barh(y, vals, color=cols, height=0.62)
for yi, v in zip(y, vals): ax.text(v + 2 if v >= 0 else 3, yi, f"{v}%", va="center", ha="left", fontsize=6.6, color=TXT)
ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=6.0); ax.invert_yaxis(); ax.set_xlim(-105, 110)
ax.axvline(0, color="#9a9a94", lw=0.8); ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(length=0)
ax.set_title("各环节公开毛利估计（%）", fontsize=8)
fig.tight_layout()
save(fig, "fig4_2_valueflow.png")

# ---------- fig5_1 segments matrix ----------
fig, ax = blank(6.3, 3.6)
cols_ = ["从零生成新项目", "在既有项目上增量开发", "维护已上线的业务系统"]
rows_ = ["专业开发者 / 企业团队", "有一定基础的独立开发者", "主要依靠自然语言的\n低编程基础用户"]
x0, y0, cw, rh = 0.20, 0.10, 0.265, 0.25
for j, c in enumerate(cols_):
    ax.text(x0 + cw * j + cw / 2, 0.90, c, ha="center", fontsize=7.5, weight="bold")
for i, r in enumerate(rows_):
    ax.text(x0 - 0.01, y0 + rh * (2 - i) + rh / 2, r, ha="right", va="center", fontsize=7)
cells = {
 (0, 0): ("IDE/CLI 智能体为主；验证手段完整", "white"),
 (0, 1): ("Cursor、Claude Code、Codex、Copilot；\n规则文件 + 测试 + PR 评审", "white"),
 (0, 2): ("CLI/云端智能体；METR：熟悉的大型仓库上\n−19%；仅 20% 用于生产排障", "white"),
 (1, 0): ("全部工具可用；\n\"一人组织\" 4%→10%", "white"),
 (1, 1): ("多工具组合；按成本切换模型", "white"),
 (1, 2): ("验证靠 diff 与手测；\n规则文件使用率低", "#fdf1ec"),
 (2, 0): ("Lovable、Replit、Bolt、Base44；\n64% \"即时成功\"体验", "white"),
 (2, 1): ("同一平台内迭代；\n20–30 条消息后上下文衰减", "#fdf1ec"),
 (2, 2): ("【本报告重点细分】产品覆盖最薄：不可导入既有仓库、无法独立验收、修复循环消耗 credit", "#fff3d6"),
}
for (i, j), (t, fc) in cells.items():
    x = x0 + cw * j; y = y0 + rh * (2 - i)
    ec = C[3] if fc == "#fff3d6" else ("#f3c9b5" if fc == "#fdf1ec" else "#dedcd6")
    ax.add_patch(Rectangle((x + 0.004, y + 0.006), cw - 0.008, rh - 0.012, fc=fc, ec=ec, lw=1.2 if fc == "#fff3d6" else 0.8))
    tt, _n = wrap_cjk(t.replace("\n", ""), 19) if "\n" not in t or len(t) > 30 else (t, 1)
    ax.text(x + cw / 2, y + rh / 2, tt, ha="center", va="center", fontsize=5.9, color=TXT, linespacing=1.25)
ax.text(0.5, 0.025, "阴影深浅表示研究证据显示的困难程度（浅橙：显著困难；深黄：本报告重点，困难最集中）", ha="center", fontsize=6.2, color=TXT2)
ax.annotate("", xy=(0.995, 0.10), xytext=(0.995, 0.85), arrowprops=dict(arrowstyle="<->", color="#9a9a94", lw=0.8))
ax.text(1.0, 0.475, "编程能力↓", rotation=90, va="center", ha="left", fontsize=6, color=TXT2)
save(fig, "fig5_1_segments.png")

# ---------- fig5_2 journey ----------
fig, ax = blank(6.3, 3.6)
stages = ["1 描述需求\n/ 报告故障", "2 定位相关代码\n与业务约束", "3 让智能体修改", "4 验证修复结果", "5 检查回归\n与数据状态", "6 记录决策\n供下次使用"]
n = len(stages); w = 0.145; gap = (1 - n * w) / (n - 1)
for i, s in enumerate(stages):
    x = i * (w + gap)
    box(ax, x, 0.70, w, 0.18, s, fc="#e9f1fc", ec=C[0], fs=6.6)
    if i < n - 1:
        arrow(ax, x + w, 0.79, x + w + gap, 0.79, color=C[0], mutation=7)
# loop arrow from 4 back to 3
arrow(ax, 3 * (w + gap) + w / 2, 0.70, 2 * (w + gap) + w / 2, 0.70, color=C[7], mutation=7, cs="arc3,rad=-0.6", ls="--")
ax.text(3 * (w + gap), 0.595, "修复循环\n（prompt spiral）", ha="center", fontsize=6, color=C[7])
arrow(ax, 5 * (w + gap) + w / 2, 0.70, 1 * (w + gap) + w / 2, 0.70, color=C[6], mutation=7, cs="arc3,rad=-0.25", ls="--")
ax.text(3.5 * (w + gap), 0.515, "下一轮任务：规则/决策是否被检索并遵循？", ha="center", fontsize=6, color=C[6])
pains = [
 "自然语言描述与代码现实不匹配；初学者低上下文提示占 28.9%",
 "既有代码 + 隐性约束；上下文衰减（32K 即降半）；生成代码不遵循既有约定",
 "\"做超出要求的事\"（8/13）；重复代码块 8 倍；修复引入新错误",
 "无法判断是否真修好：36% 跳过 QA；AI 自报\"测试通过\"可能不实（作弊率 46–76%）",
 "回滚不含数据库；RLS 等安全配置无感知；\"修一处坏一处\"",
 "规则文件遵循率无数据；过长即失效；多轮后\"失忆\"",
]
srcs = ["[134]", "[117][125][140]", "[133][125][137]", "[131][110][147]", "[136][151]", "[84][119][144]"]
for i, (p, s) in enumerate(zip(pains, srcs)):
    x = i * (w + gap)
    t, nl = wrap_cjk(p, 10.8)
    ax.add_patch(Rectangle((x, 0.14), w, 0.32, fc="#fff8f4", ec="#f3c9b5", lw=0.7))
    ax.text(x + w / 2, 0.445, t, ha="center", va="top", fontsize=5.4, color=TXT, linespacing=1.2)
    ax.text(x + w / 2, 0.155, s, ha="center", fontsize=5.4, color=MUTED)
ax.text(0.0, 0.475, "痛点与证据", fontsize=6.5, color=C[1], weight="bold", va="bottom")
ax.text(0.0, 0.94, "任务旅程（维护已有 Web 应用）", fontsize=6.5, color=C[0], weight="bold")
ax.text(1.0, 0.94, "工具减少：写代码、查资料 | 转移给用户：验证、回归检查、上下文维护、成本控制", fontsize=5.8, color=TXT2, ha="right")
save(fig, "fig5_2_journey.png")

# ---------- fig5_3 QA practices + METR ----------
fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.8), gridspec_kw={"width_ratios": [1.15, 1]})
ax = axes[0]
labels = ["跳过 QA", "手动测试或手改", "无条件信任", "把 QA 委托给 AI", "其他/未说明"]
vals = [36, 29, 18, 10, 7]
cols = [C[7], C[2], C[1], C[3], "#c8c7c1"]
y = np.arange(len(labels))
ax.barh(y, vals, color=cols, height=0.62)
for yi, v in zip(y, vals): ax.text(v + 0.8, yi, f"{v}%", va="center", fontsize=7.5)
ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=7.5); ax.invert_yaxis(); ax.set_xlim(0, 45)
ax.set_title("低基础用户的质量保证实践（n=518 条记录）", fontsize=8); ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(length=0)
ax.text(44, 4.7, "\"其他\"为 100% 减各项所得；自选择样本，不可泛化", fontsize=5.5, color=MUTED, ha="right", va="top")
ax = axes[1]
labels = ["事前预期", "事后自评", "ML 专家\n预测", "实测\n（RCT）"]
vals = [-24, -20, -38, 19]
cols = [C[0], C[0], C[0], C[7]]
ax.bar(np.arange(4), vals, color=cols, width=0.6)
for i, v in enumerate(vals): ax.text(i, v + (1.5 if v > 0 else -4), f"{v:+d}%", ha="center", fontsize=7.5)
ax.axhline(0, color="#9a9a94", lw=0.8)
ax.set_xticks(np.arange(4)); ax.set_xticklabels(labels, fontsize=7); ax.set_ylim(-48, 30)
ax.set_ylabel("任务耗时变化（%）", fontsize=7.5); tidy(ax)
ax.set_title("METR RCT：感知 vs 实测（n=16）", fontsize=8)
ax.text(1.5, 25, "95% CI +2% 至 +39%", ha="center", fontsize=6.3, color=TXT2)
fig.tight_layout()
save(fig, "fig5_3_qa.png")

# ---------- fig_caseA Replit timeline ----------
fig, ax = blank(6.3, 2.6)
evs = [("07-12", "Lemkin 开始 12 天实验，\n数小时做出原型"), ("07-17", "称自己已\"hooked\""), ("07-18", "代码冻结期间智能体\n删除生产数据库"), ("07-19", "Lemkin 自行回滚成功\n（智能体曾称不可回滚）"), ("07-20", "再次违反冻结；\nCEO Masad 回应"), ("07-21/22", "媒体报道；Replit\n公布整改措施")]
n = len(evs); xs = np.linspace(0.06, 0.94, n)
ax.plot([0.02, 0.98], [0.55, 0.55], color="#9a9a94", lw=1.2)
for i, (dd, t) in enumerate(evs):
    c = C[7] if i in (2, 4) else (C[2] if i == 3 else C[0])
    ax.plot(xs[i], 0.55, "o", color="white", mec=c, mew=1.8, ms=7, zorder=3)
    ax.text(xs[i], 0.63, "2025-" + dd, ha="center", fontsize=6.5, weight="bold", color=c)
    ax.text(xs[i], 0.47, t, ha="center", va="top", fontsize=5.9, color=TXT, linespacing=1.2)
ax.text(0.5, 0.95, "Replit Agent 删除 SaaStr 数据库事件（2025 年 7 月）", ha="center", fontsize=8, weight="bold")
ax.add_patch(Rectangle((0.02, 0.0), 0.96, 0.245, fc="#e9f1fc", ec=C[0], lw=0.8))
ax.text(0.03, 0.225, "厂商整改（Masad 帖子与 Replit 博客）：① 自动开发/生产数据库分离  ② 一键恢复整个项目状态  ③ 规划/仅聊天模式\n④ 强制智能体检索内部文档  ⑤ Staging 环境（在研）", fontsize=5.8, va="top", color=TXT, linespacing=1.3)
ax.text(0.03, 0.115, "可支持的判断：自然语言指令不是安全控制；模型对自身能力的陈述不可信；产品层可恢复性比模型\"承诺\"重要。\n局限：细节来自当事人单方陈述，未公开完整会话记录。", fontsize=5.8, va="top", color=TXT2, linespacing=1.3)
save(fig, "fig_caseA.png")

# ---------- fig_caseB Lovable chain ----------
fig, ax = blank(6.3, 2.5)
evs = [("2025-03-21", "Palmer 报告 RLS 缺失\n（170 项目/303 端点）", C[7]), ("2025-04-24", "Lovable 2.0 加入\n安全扫描（仅查 RLS 存在）", C[0]), ("2025-05-29", "CVE-2025-48757 发布\n（CVSS 9.3，有争议）", C[7]), ("2026-02-27", "Khan：推广应用\n暴露 18,697 条记录", C[7]), ("2026-04-20", "平台 API 所有权校验缺陷；\nLovable 先否认后承认", C[7]), ("2026-08-10", "Quick scan 每次发布\n自动运行（不可关闭）", C[0]), ("2026-09-26", "UpGuard：16,326 个\nSupabase 库公开可读", C[1])]
n = len(evs); xs = np.linspace(0.05, 0.95, n)
ax.plot([0.02, 0.98], [0.50, 0.50], color="#9a9a94", lw=1.2)
for i, (dd, t, c) in enumerate(evs):
    ax.plot(xs[i], 0.50, "o", color="white", mec=c, mew=1.8, ms=7, zorder=3)
    up = i % 2 == 0
    ax.text(xs[i], 0.58 if up else 0.42, dd, ha="center", va="bottom" if up else "top", fontsize=6.2, weight="bold", color=c)
    ax.text(xs[i], 0.69 if up else 0.31, t, ha="center", va="bottom" if up else "top", fontsize=5.7, color=TXT, linespacing=1.2)
ax.text(0.5, 0.97, "Lovable 生成应用的 RLS 缺失：从 CVE 到平台级缺陷（2025-03 至 2026-09）", ha="center", fontsize=8, weight="bold")
ax.legend(handles=[Patch(color=C[7], label="漏洞披露 / 泄露"), Patch(color=C[0], label="厂商产品响应"), Patch(color=C[1], label="行业范围扫描")], loc="lower center", ncol=3, frameon=False, fontsize=6.3, bbox_to_anchor=(0.5, 0.0))
save(fig, "fig_caseB.png")

# ---------- fig6_1 architectures ----------
fig, ax = blank(6.3, 3.9)
cols_ = ["IDE 内嵌助手", "AI 原生 IDE", "终端/CLI 智能体", "云端异步智能体", "一体化平台"]
rows_ = ["执行环境", "仓库工作方式", "验证闭环", "风险边界", "代表产品"]
cells = [
 ["本地 IDE + 终端；\n云代理用临时环境", "本地终端 + 内置浏览器；\n可选云 VM", "本地 shell（可选 OS 沙箱）\n+ 浏览器扩展 + MCP", "云容器/VM，\n网络默认受限", "平台内运行时\n（容器 / WebContainers / 沙箱）"],
 ["用户 Git 仓库；\n云代理开分支 + PR", "用户 Git 仓库", "用户 Git 仓库；\n可选云会话", "克隆仓库 → 分支 → PR", "平台内项目；\n可同步/导出 GitHub"],
 ["用户自测 + CI；\nPlaywright MCP", "终端 + Browser 工具；\nCheckpoints（仅文件）", "测试命令 + Chrome/\nComputer Use；/rewind", "容器内测试 + 内置浏览器；\nPR 评审", "智能体自测（真实浏览器）\n+ 安全扫描；版本 revert"],
 ["分支保护；防火墙", "默认需审批", "沙箱默认关；auto 模式\n由分类器审查", "代理阶段断网；\n59 分钟上限", "DB 不随版本回滚；\n扫描\"提示 + 用户决定\""],
 ["Copilot、Qoder CN、\nCodeBuddy", "Cursor、Devin Desktop、\nTrae、Kiro", "Claude Code、Codex、\nAider、OpenCode", "Codex cloud、Copilot cloud\nagent、Devin、Jules", "Lovable、Replit、Bolt、\nv0、Base44"],
]
x0, y0, cw, rh = 0.13, 0.02, 0.174, 0.168
for j, c in enumerate(cols_):
    ax.add_patch(Rectangle((x0 + cw * j + 0.003, 0.87), cw - 0.006, 0.10, fc=C[0], ec=C[0]))
    ax.text(x0 + cw * j + cw / 2, 0.92, c, ha="center", va="center", fontsize=6.8, color="white", weight="bold")
for i, r in enumerate(rows_):
    y = y0 + rh * (4 - i)
    ax.add_patch(Rectangle((0.0, y + 0.003), 0.125, rh - 0.006, fc=LIGHT, ec="#dedcd6"))
    ax.text(0.0625, y + rh / 2, r, ha="center", va="center", fontsize=6.6, weight="bold")
    for j in range(5):
        x = x0 + cw * j
        fc = "#fff8f4" if (i == 3 and j == 4) or (i == 2 and j == 4) else "white"
        ax.add_patch(Rectangle((x + 0.003, y + 0.003), cw - 0.006, rh - 0.006, fc=fc, ec="#dedcd6", lw=0.7))
        ax.text(x + cw / 2, y + rh / 2, cells[i][j], ha="center", va="center", fontsize=5.1, color=TXT, linespacing=1.2)
save(fig, "fig6_1_arch.png")

# ---------- fig6_2 verify matrix heatmap ----------
fig, ax = plt.subplots(figsize=(6.3, 3.0))
prods = ["Claude Code", "Codex", "Cursor", "Copilot cloud agent", "Replit Agent", "Lovable", "Kiro", "Aider / OpenCode"]
mechs = ["读取日志", "运行测试/终端", "浏览器/预览交互", "diff 审查", "检查点/回滚", "安全扫描", "CI 集成"]
# 2 full, 1 partial, 0 none, -1 unverified
M = np.array([
 [2, 2, 2, 2, 1, 2, 2],
 [2, 2, 2, 2, -1, 1, 2],
 [2, 2, 2, 2, 1, 1, 2],
 [2, 2, 1, 2, 1, 2, 2],
 [2, 2, 2, 1, 2, 1, 1],
 [1, 1, 1, 1, 1, 2, 1],
 [2, 2, -1, 2, 1, -1, 0],
 [2, 2, 0, 1, 2, 0, 0],
])
from matplotlib.colors import ListedColormap
cmap = ListedColormap(["#f1f0ec", "#f4f3ef", "#b7d0f0", "#2a78d6"])
ax.imshow(M + 1, cmap=cmap, vmin=0, vmax=3, aspect="auto")
ax.set_xticks(range(len(mechs))); ax.set_xticklabels(mechs, fontsize=7, rotation=20, ha="right")
ax.set_yticks(range(len(prods))); ax.set_yticklabels(prods, fontsize=7.5)
for i in range(len(prods)):
    for j in range(len(mechs)):
        v = M[i, j]
        txt = {2: "完整", 1: "部分", 0: "—", -1: "未核实"}[v]
        ax.text(j, i, txt, ha="center", va="center", fontsize=6.3, color="white" if v == 2 else TXT2)
ax.set_xticks(np.arange(-0.5, len(mechs), 1), minor=True); ax.set_yticks(np.arange(-0.5, len(prods), 1), minor=True)
ax.grid(which="minor", color="white", lw=2); ax.tick_params(length=0, which="both")
for s in ax.spines.values(): s.set_visible(False)
ax.text(len(mechs) - 0.5, -0.9, "评分依据官方文档（2026-10-14）：完整=智能体可直接调用且面向该产品主要用户；部分=需手动触发/仅限部分计划或数据面不完整", fontsize=5.6, color=MUTED, ha="right")
fig.tight_layout()
save(fig, "fig6_2_verify_matrix.png")

# ---------- fig6_3 memory layers ----------
fig, ax = blank(6.3, 3.6)
layers = [
 ("① 信息保存", C[2], "供给充分", "规则文件：AGENTS.md（60,000+ 项目）、CLAUDE.md、.cursor/rules、copilot-instructions、Lovable Knowledge、replit.md\n持久记忆：Claude Code Auto memory、Copilot Memory、Codex Memories（默认关）\n任务记录：Task 工具、Kiro tasks.md、Cursor Projects", "限制：Claude Code 建议 <200 行；Codex 合并上限 32 KiB；Lovable 10,000 字符；Devin Local 不持久化记忆"),
 ("② 正确检索", C[3], "依赖窗口与压缩\n已知衰减", "代码库检索：Cursor Instant Grep + Explore 子智能体（已弃用 embedding）；Claude Code agentic search + LSP；Copilot 远程语义索引；Devin DeepWiki\n上下文：1M 窗口，约 967K 自动压缩；压缩后重载规则与记忆、重读 5 个文件", "研究：Context Rot（18 模型，聚焦提示远优于完整提示）；NoLiMa 32K 即降半；多轮对话平均 −39%"),
 ("③ 实际遵循", C[7], "证据最弱\n结论偏负", "官方：规则文件是\"上下文而非强制配置\"；过长即被忽略；长对话中不一定一致遵循\n可执行层：hook（PreToolUse）、CI、lint 是硬性阻止的唯一手段", "研究：上下文文件总体不提升成功率（成本 +20%），但明确指令遵循良好 [119]；288 次运行无可测影响 [120]；执行化后合规率 67% → 88.3% [121]"),
]
y = 0.70
for title, c, verdict, supply, note in layers:
    ax.add_patch(Rectangle((0.0, y), 0.16, 0.27, fc=c, ec=c))
    ax.text(0.08, y + 0.19, title, ha="center", va="center", fontsize=8, color="white", weight="bold")
    ax.text(0.08, y + 0.075, verdict, ha="center", va="center", fontsize=6, color="white", linespacing=1.3)
    ax.add_patch(Rectangle((0.165, y), 0.835, 0.27, fc="white", ec="#dedcd6"))
    t1, n1 = wrap_cjk(supply, 60)
    ax.text(0.175, y + 0.255, t1, fontsize=5.6, va="top", color=TXT, linespacing=1.22)
    t2, n2 = wrap_cjk(note, 60)
    ax.text(0.175, y + 0.095, t2, fontsize=5.6, va="top", color=C[7] if "研究" in note[:2] else TXT2, linespacing=1.22)
    if y > 0.1:
        arrow(ax, 0.08, y, 0.08, y - 0.04, color="#6f6e69", mutation=7)
    y -= 0.31
ax.text(0.5, 0.025, "结论：供给在\"保存\"层解决了\"记住我说过的话\"，但尚未解决\"按我说过的话行动\"；不可违反的约束需落到可执行层", ha="center", fontsize=6.3, color=TXT2)
save(fig, "fig6_3_memory_layers.png")

# ---------- fig6_4 METR horizon ----------
fig, ax = plt.subplots(figsize=(6.3, 2.8))
models = ["Claude Opus 4.5\n(2025-11)", "GPT-5.2 high\n(2025-12)", "Claude Opus 4.6\n(2026-02)", "GPT-5.3-Codex high\n(2026-02)", "Gemini 3.1 Pro\n(2026-03)", "GPT-5.4 xhigh\n(2026-03)"]
h50 = [5 + 20/60, 6 + 34/60, 11 + 59/60, 6.5, 5 + 50/60, 5 + 42/60]
h80 = [42/60, 55/60, 1 + 10/60, 47/60, 1.5, 54/60]
x = np.arange(len(models)); w = 0.36
ax.bar(x - w/2, h50, w, color=C[0], label="50% 成功率地平线")
ax.bar(x + w/2, h80, w, color=C[1], label="80% 成功率地平线")
for xi, v in zip(x - w/2, h50): ax.text(xi, v + 0.2, f"{v:.1f}h", ha="center", fontsize=6.5)
for xi, v in zip(x + w/2, h80): ax.text(xi, v + 0.2, f"{int(v*60)}m", ha="center", fontsize=6.5)
ax.set_xticks(x); ax.set_xticklabels(models, fontsize=6.3); ax.set_ylabel("人类任务时长（小时）"); ax.set_ylim(0, 14)
tidy(ax); ax.legend(frameon=False, fontsize=7, loc="upper left")
ax.text(5.3, 12.5, "80% 地平线约为 50% 的 1/5–1/10：\n\"有一半概率完成\"与\"可放心交付\"之间的差距", ha="right", fontsize=6.3, color=TXT2)
save(fig, "fig6_4_horizon.png")

# ---------- fig7_1 landscape ----------
fig, ax = blank(6.3, 3.8)
cols_ = ["IDE 内嵌助手", "AI 原生 IDE", "终端/CLI 智能体", "云端异步智能体", "一体化平台"]
rows_ = ["企业 / 专业开发者", "独立开发者", "低编程基础用户"]
x0, y0, cw, rh = 0.16, 0.05, 0.166, 0.27
for j, c in enumerate(cols_):
    ax.text(x0 + cw * j + cw / 2, 0.90, c, ha="center", fontsize=7, weight="bold")
for i, r in enumerate(rows_):
    ax.text(x0 - 0.01, y0 + rh * (2 - i) + rh / 2, r, ha="right", va="center", fontsize=6.8)
    for j in range(5):
        ax.add_patch(Rectangle((x0 + cw * j, y0 + rh * (2 - i)), cw, rh, fc="white" if (i + j) % 2 == 0 else "#faf9f6", ec="#e6e5e0", lw=0.6))
# bubbles: (col,row, size, label, color)
bub = [
 (0, 0, 58.7, "GitHub Copilot\n58.7%", C[0]), (0, 0.9, 0, "", C[0]),
 (1, 0.15, 25.5, "Cursor 25.5%\n（ARR $40 亿+）", C[0]), (1, 0.95, 6.5, "Devin Desktop\n(Windsurf) 6.5%", C[0]),
 (2, 0.0, 65.5, "Claude Code\n65.5%", C[0]), (2, 0.95, 29.5, "Codex 29.5%", C[0]), (2, 1.75, 13.6, "OpenCode 13.6%", C[0]),
 (3, 0.1, 16.0, "Antigravity 16.0%\nJules 2.5%", C[0]), (3, 0.95, 2.9, "Devin 2.9%", C[0]),
 (4, 0.2, 12, "Replit（ARR ~$5 亿）\nSO 使用率 2.3%", C[1]), (4, 1.95, 14, "Lovable（ARR ~$6 亿）\n80% 非技术用户", C[1]), (4, 1.2, 6, "Bolt、v0、Base44", C[1]),
 (0, 1.6, 10, "中国：Qoder CN、\nCodeBuddy、文心快码", C[2]), (1, 1.75, 8, "Trae 1.3%\nQoder、Kiro", C[2]),
]
for (j, ri, s, lab, c) in bub:
    if s == 0: continue
    cx = x0 + cw * j + cw / 2; cy = y0 + rh * (2 - ri) + rh / 2
    r = 0.010 + 0.0016 * s ** 0.85
    ax.scatter([cx], [cy + 0.03], s=(r * 6.3 * 72) ** 2 * 3.1416 * 0.9, color=c, edgecolor="white", alpha=0.85, zorder=3)
    ax.text(cx, cy + 0.03 - r * 1.05 - 0.04, lab, ha="center", va="top", fontsize=5.4, color=TXT, zorder=4, linespacing=1.15)
ax.legend(handles=[Patch(color=C[0], label="使用率口径（SO 2026，专业开发者）"), Patch(color=C[1], label="收入口径（一体化平台，公司自述/估计）"), Patch(color=C[2], label="中国市场（IDC 收入份额 / Trae 自报）")], loc="lower center", bbox_to_anchor=(0.5, -0.04), ncol=3, frameon=False, fontsize=6)
ax.text(0.5, 0.955, "气泡大小仅示意，不同口径不可直接比较；位置示意产品的主要用户群", ha="center", fontsize=6, color=MUTED)
save(fig, "fig7_1_landscape.png")

# ---------- fig7_2 usage bar ----------
fig, ax = plt.subplots(figsize=(6.3, 3.0))
tools = ["Claude Code", "GitHub Copilot", "OpenAI Codex", "Cursor", "Google Antigravity", "Gemini Code Assist", "OpenCode", "JetBrains AI", "Windsurf", "Cline", "Devin", "Jules", "Replit Agent", "Aider", "Trae"]
vals = [65.5, 58.7, 29.5, 25.5, 16.0, 14.6, 13.6, 12.8, 6.5, 4.5, 2.9, 2.5, 2.3, 2.1, 1.3]
owner = ["模型厂商自营", "平台巨头", "模型厂商自营", "被平台收购", "模型厂商自营", "模型厂商自营", "开源", "独立/IDE 厂商", "被收购", "开源", "独立", "模型厂商自营", "一体化平台", "开源", "平台巨头"]
cm = {"模型厂商自营": C[0], "平台巨头": C[6], "被平台收购": C[3], "被收购": C[3], "开源": C[2], "独立/IDE 厂商": "#c8c7c1", "独立": "#c8c7c1", "一体化平台": C[1]}
y = np.arange(len(tools))
ax.barh(y, vals, color=[cm[o] for o in owner], height=0.65)
for yi, v in zip(y, vals): ax.text(v + 0.6, yi, f"{v}%", va="center", fontsize=6.8)
ax.set_yticks(y); ax.set_yticklabels(tools, fontsize=7); ax.invert_yaxis(); ax.set_xlim(0, 75)
ax.set_xlabel("过去一年使用过的受访者比例（%，多选）", fontsize=7.5)
ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(length=0)
ax.legend(handles=[Patch(color=C[0], label="模型厂商自营"), Patch(color=C[6], label="平台巨头（微软/字节）"), Patch(color=C[3], label="被平台收购（SpaceX/Cognition）"), Patch(color=C[2], label="开源"), Patch(color=C[1], label="一体化平台"), Patch(color="#c8c7c1", label="独立公司")], loc="lower right", frameon=False, fontsize=6.3)
save(fig, "fig7_2_usage.png")

# ---------- fig7_3 five forces ----------
fig, ax = blank(6.3, 4.2)
def force(x, y, w, h, title, level, lc, items):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=lc, lw=1.4))
    ax.add_patch(Rectangle((x, y + h - 0.075), w, 0.075, fc=lc, ec=lc))
    ax.text(x + 0.01, y + h - 0.0375, f"{title}：{level}", fontsize=7, color="white", weight="bold", va="center")
    yy = y + h - 0.09
    for it in items:
        t, n = wrap_cjk(it, w * 6.3 * 72 / 5.5 * 0.80)
        ax.text(x + 0.01, yy, "• " + t, fontsize=5.5, va="top", color=TXT, linespacing=1.2)
        yy -= 0.027 * n + 0.01
force(0.33, 0.68, 0.34, 0.30, "供应商（模型）议价能力", "强", C[7], ["Windsurf 断供（2025-06）；OpenAI 对 Cursor 断供（2026-11 生效）", "Cursor 2025 年中约 130% 收入付给 Anthropic；优先服务层使账单翻倍", "弱化因素：开源/低价模型（DeepSeek、Kimi、Qwen）；Copilot 六家模型可选"])
force(0.33, 0.33, 0.34, 0.30, "现有竞争者", "强而集中", C[1], ["SO 2026 前四名使用率均 >25%（Claude Code、Copilot、Codex、Cursor）", "三大模型厂商直接下场；头部应用层被平台持有或自研模型", "中国厂商 2026 年由免费转收费并提价"])
force(0.0, 0.33, 0.30, 0.30, "新进入者威胁", "两极", C[3], ["低：开源智能体（Aider、OpenCode）、模型 API、Base44 六人团队被收购", "高：负毛利期需数十亿美元融资；算力与接入权受制于巨头；Copilot 冻结注册 58 天"])
force(0.70, 0.33, 0.30, 0.30, "替代品威胁", "中高", C[6], ["直接用 ChatGPT/Claude 聊天（ChatGPT 使用率 41%）", "低代码/无代码平台（Wix 收购 Base44）", "外包与自由职业者（修复服务）"])
force(0.33, 0.0, 0.34, 0.30, "买方议价能力 / 迁移成本", "中等偏低", C[2], ["低迁移成本：GitHub 导出、AGENTS.md 与 MCP 标准化、多云计费", "高迁移成本：平台不可导入已有仓库；工具特定 hook/技能；企业席位合约（Cursor 75% 收入）", "质量优先于成本：仅 6.4% 因成本切换"])
for (x1, y1, x2, y2) in [(0.50, 0.68, 0.50, 0.63), (0.30, 0.48, 0.33, 0.48), (0.70, 0.48, 0.67, 0.48), (0.50, 0.30, 0.50, 0.33)]:
    arrow(ax, x1, y1, x2, y2, color="#6f6e69", mutation=8, lw=1.2)
save(fig, "fig7_3_fiveforces.png")

# ---------- fig7_4 pricing shift ----------
fig, ax = blank(6.3, 3.0)
rows = [
 ("Cursor", "2025-06-16", "Pro 500 次快速请求 → $20 用量池按 API 价扣减；7-07 道歉退款", C[0]),
 ("Claude Code", "2025-08-28", "Pro/Max 增加每周上限；2026-06-15 程序化用量单独计费", C[1]),
 ("Replit", "2025-07-01", "每 checkpoint 固定 $0.25 → effort-based（大任务打包为更贵 checkpoint）", C[2]),
 ("OpenAI Codex", "2026-04-02/09", "改按 token 计费；新增 $100 Pro 档（5x Plus）", C[3]),
 ("GitHub Copilot", "2026-04-20 → 06-17", "暂停个人新注册 58 天 → 全线 AI Credits（$0.01/credit）→ 新增 $100 Max", C[6]),
 ("Gemini CLI", "2026-06-18", "免费层/个人账号迁至 Antigravity CLI，配额多次下调", C[7]),
 ("Qoder / 灵码 / CodeBuddy", "2026-04/05", "结束五折与免费试用；企业版提价 >100%", C[4]),
]
ax.text(0.0, 0.97, "产品", fontsize=7, weight="bold", va="top"); ax.text(0.25, 0.97, "时间", fontsize=7, weight="bold", va="top"); ax.text(0.42, 0.97, "变化", fontsize=7, weight="bold", va="top")
y = 0.86
for p, t, desc, c in rows:
    ax.add_patch(Rectangle((0.0, y - 0.05), 1.0, 0.115, fc="white", ec="#e6e5e0", lw=0.6))
    ax.add_patch(Rectangle((0.0, y - 0.05), 0.012, 0.115, fc=c, ec=c))
    ax.text(0.025, y + 0.008, p, fontsize=6.5, va="center", weight="bold")
    ax.text(0.25, y + 0.008, t, fontsize=6.3, va="center", color=TXT2)
    tt, n = wrap_cjk(desc, 46)
    ax.text(0.42, y + 0.008, tt, fontsize=6.0, va="center", linespacing=1.2)
    y -= 0.125
ax.text(0.5, 0.0, "共同方向：从\"席位订阅、无限使用\"转向\"订阅 + 用量透传 / 抽象 credit\"，并新增 $100 高价档；推理成本风险由厂商转向用户", ha="center", fontsize=6.2, color=TXT2, va="bottom")
save(fig, "fig7_4_pricing.png")

# ---------- fig8_1 risk matrix ----------
fig, ax = plt.subplots(figsize=(6.3, 3.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.set_xlabel("发生可能性（定性）"); ax.set_ylabel("对独立开发者与小团队的影响（定性）")
ax.axhline(5, color="#dedcd6", lw=0.8); ax.axvline(5, color="#dedcd6", lw=0.8)
risks = [
 ("模型供应中断\n（并购/竞争关系变化）", 6.2, 7.4, C[7]),
 ("成本失控\n（长会话、多智能体、修复循环）", 8.5, 6.5, C[1]),
 ("安全与数据泄露\n（非技术用户部署公开应用）", 8.4, 9.1, C[7]),
 ("\"AI 自报成功\"被证伪\n引发信任崩塌", 4.3, 7.3, C[3]),
 ("法律与版权\n（许可证合同诉求未决）", 2.6, 4.3, C[6]),
 ("监管与备案\n（中国面向公众服务）", 4.6, 2.5, C[0]),
 ("免费/低价层收缩", 8.8, 4.2, C[2]),
 ("平台锁定与不可导入", 6.5, 5.2, C[4]),
]
for t, x, y, c in risks:
    ax.scatter(x, y, s=260, color=c, alpha=0.85, zorder=3, edgecolor="white")
    ax.text(x, y - 0.62, t, ha="center", va="top", fontsize=6, color=TXT, linespacing=1.15)
ax.text(9.8, 9.6, "高可能性 · 高影响", ha="right", fontsize=7, color=TXT2); ax.text(0.2, 9.6, "低可能性 · 高影响", fontsize=7, color=TXT2)
ax.text(9.8, 0.3, "高可能性 · 低影响", ha="right", fontsize=7, color=TXT2); ax.text(0.2, 0.3, "低可能性 · 低影响", fontsize=7, color=TXT2)
ax.set_xticks([]); ax.set_yticks([])
save(fig, "fig8_1_risk_matrix.png")
