---
name: industry-research-deck
description: 就任何一个行业做市场调研并生成一套幻灯片（Slides 工件）：证据分级、图表自查、编辑式版式、风格样张与背景手法。用户说“做某行业的调研报告 PPT / 市场分析幻灯片”时使用。
---

# industry-research-deck

把一个行业调研从取证到成片做成 16:9 幻灯片。流程分六步，每步有验收点。

## 1. 立题与证据规则（先定，后找）
- 确认：行业边界、目标读者、章节骨架（默认 8 章：定义与边界 / 发展与规模 / PEST / 产业链 / 用户与案例 / 技术与产品 / 竞争格局 / 风险与预测）。
- 证据分五类并全程标注：**实际值 / 估计 / 预测 / 厂商自述 / 推断**。不同口径的市场规模不能相加；不编排名；不做 STP/4P 与创业建议。
- 每条结论配证据强度：强（多类独立证据一致）/ 中（样本有限或依赖估计）/ 弱（主要基于推断）。

## 2. 取证
- 先连接器与 WebSearch，再 WebFetch 原文；每个数字记录来源编号 [n]、口径、年份、样本量。
- 机构预测与厂商收入自下而上互相校验，差两个数量级要写明。
- 产出 `content/*.md`（报告正文方言：TABLE/FIG 标记、`{#key w=.. fs=.. split keep}` 表格选项）。

## 3. 图表（matplotlib，`figs/common.py` 统一风格）
- 一图一结论：标题是一句话结论，不是“XX 情况”。
- 中文换行用 `wrap_cjk`（含标点避头尾）；`figaudit.py` 检查重叠/溢出/最小字号。
- 幻灯片版重出：`figs_deck.py` + `deck_cfg.json`（每图宽×/高×/字号×，默认 1.45/1.08/1.32），纸色底 #F6F3EC；`figs_variants.py dark|mono` 出暗色/单色版。

## 4. 成片（Slides 工件类型）
- 一页一句话结论 + 一张图；注释进 `<aside>` 讲稿。表格超过 6 行拆页。
- 编辑式视觉系统（默认）：纸 #F6F3EC、墨 #1A1D22、灰 #5A5F66、细线 #D6D2C8、强调 #244B74、暖色 #B9462B 只给风险/限制、深色 #15212E。标题 Noto Serif SC ≤2 行 46px，正文 Noto Sans SC，标签 IBM Plex Mono / JetBrains Mono。
- 页结构：顶栏（章节标签左、图号右）→ 细线 → 标题 → 图 1664×560–600 contain → 页脚（来源左 1300px，“证据强度 · n/N”右，bottom:64px）。章节分隔页：260px 衬线大数字 + 事实/机制/判断三行。
- 写法：每页一个 `project/slides/<id>.html`，内联样式闭合子集（px、hex，无渐变/阴影/z-index）；底图用上传资产 `/_blob/<id>`，放在 section 第一个子元素；**全出血底图之上的正文要整体装进一个 `position:absolute` 的容器**，否则会被底图盖住。

## 5. 风格样张（用户要“更有审美 / 少 AI 感”时）
- 先做 4 个方向 × 4 种页型（分隔/关键数字/图页/发现页）的样张册，再套全册：
  A 暗室（dark.design、Linear/Vercel；#0B0D10 + Space Grotesk + 等宽标签）/ B 海报（recent.design、loadmo.re；900 字重巨数字、4px 粗线、整页朱红陈述页）/ C 极简（minimal.gallery、瑞士网格；纯白无线条、两级灰）/ D 暖调（Typewolf Daylight；杏色 #F3E3C8 + 橄榄绿 #3F4A2E 左侧整栏）。
- 背景手法（从 UI 设计借，静态可用）：E1 点阵网格+标尺+幽灵数字；E2 连接线示意图当底；E3 曲线去字压暗做底；E4 层叠窗口框；E5 上下色块分割；E6 光晕+颗粒。用量：一页一种、全册不超过三种、背景对比度低于正文。底图用 PIL 生成 PNG/JPEG 资产（`styles/bg/gen_bg.py`）。

## 6. 自查（用户允许时）
- 本地 Chromium（Playwright）按 1920×1080 渲染每页：`render.py`/`render_s.py` 报告正文触底、溢出、标题行数>2；拼接 contact sheet 人眼复核。
- 只修报告的问题，先列清单再改；改完再跑一次。
