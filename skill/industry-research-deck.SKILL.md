---
name: industry-research-deck
description: 就任何一个行业做市场调研并生成一套幻灯片（Slides 工件）：证据分级、图表自查、编辑式版式、风格样张与背景手法。用户说“做某行业的调研报告 PPT / 市场分析幻灯片”时使用。
---

# industry-research-deck

把一个行业调研从取证到成片做成 16:9 幻灯片。六步，每步有验收点；脚本与模板在 PPT_design 仓库（`report/`、`decks/`、`tools/`），本文给出不看脚本也能复现的要点。

## 0. 开工前
- 先回一句话说明将做什么，再建任务清单（取证 / 图表 / 成片 / 样张 / 自查）。
- 确认三件事：行业边界、读者、输出（默认 Slides 工件；用户要 DOCX/PDF 才走报告流水线）。
- 用户给了帖子/参考站点时：用内置浏览器逐站浏览（容器网络出不去），截屏记录每站可借的版式元素，再动手。

## 1. 立题与证据规则
- 章节骨架（默认 8 章）：定义与边界 / 发展与规模 / PEST 宏观 / 产业链与价值分配 / 用户与细分（含案例）/ 技术与产品 / 竞争格局（五力）/ 风险与预测。
- 证据五类全程标注：**实际值 / 估计 / 预测 / 厂商自述 / 推断**。不同口径的市场规模不能相加；不编排名；不做 STP/4P 与创业建议。
- 每条结论配证据强度：强（多类独立证据一致）/ 中（样本有限或依赖估计）/ 弱（主要基于推断）。
- 每章开头写 `KEYPOINTS … ENDKEY`：三行“事实 | 机制 | 判断”，后面分隔页和讲稿直接复用。

## 2. 取证
- 连接器 → WebSearch → WebFetch 原文；每个数字记：来源编号 [n]、口径、年份、样本量 n。
- 机构预测 vs 厂商收入自下而上互相校验，差两个数量级就写明“口径不同”。
- 正文写成 `content/NN_chX.md`，方言标记：`COVER/TITLE:/SUBTITLE:/META:`、`# 第X章`、`KEYPOINTS…ENDKEY`、`DEF:`、`GAP:`（证据缺口）、`SOURCE:`、`PAGEBREAK`、`LANDSCAPE/PORTRAIT`（节方向）、`FIG: {#key} 标题 | 来源`、`TABLE: {#key w=列宽% fs=字号 split|keep|tail} 标题`（`keep` 整表不拆页，`tail` 允许末行跟下页，`^` 纵向合并，`brk()` 给长词插零宽断点）。
- 报告流水线（需要 DOCX/PDF 时）：`node build2.js` → `post.py` → soffice 转 PDF → `toc_gen.py fill` 跑三遍直到目录稳定 → `rowcheck.py docx pdf` 核对每个表格行都出现在 PDF（LibreOffice 会吞 tblHeader+cantSplit 的行）。

## 3. 图表（matplotlib，`figs/common.py` 统一风格）
- 一图一结论：图题是一句话结论，不是“XX 情况”；来源与口径写在图下。
- 中文换行用 `wrap_cjk`（含标点避头尾）；颜色只用调色板 `C`，暖色只给风险/限制。
- `figaudit.py`：对每张图测文本框重叠、超出画布、按版面缩放后的最小印刷字号（报告 ≥7pt，幻灯片投影 ≥18pt 等效）；先列清单，用户确认后再改。
- 幻灯片版重出：`figs_deck.py` 读 `deck_cfg.json`（`{"default":[宽×,高×,字号×], "figX.png":[…]}`，默认 1.45/1.08/1.32，密图用 1.5/1.3/1.2），底色 #F6F3EC；`figs_variants.py dark|mono` 出暗色/单色版给其他风格方向。

## 4. 成片（Slides 工件）
- 先 `list` Design System，有默认就用；没有则用下面的编辑式系统。创建工件后 deck.json + 封面先发，之后每次三页。
- 页型与规则：
  - 一页一句话结论 + 一张图；图注、数据细节进 `<aside>` 讲稿（≤4000 字）。表格超过 6 行拆页。
  - 色：纸 #F6F3EC、墨 #1A1D22、灰 #5A5F66、细线 #D6D2C8、强调 #244B74、暖 #B9462B（只给弱/限制/风险）、深 #15212E。
  - 字：标题 Noto Serif SC 600 46px ≤2 行（width 1560）；正文 Noto Sans SC 20–23px；标签 IBM Plex Mono 20px letter-spacing 2px。
  - 图页结构：顶栏（`02 — 章名` 左、`图 2-4` 右）→ `<hr width 1664 #D6D2C8>` → h2 → `<img width 1664 height 560–600 object-fit:contain>` → 页脚两条 `position:absolute;bottom:64px`（来源左 width 1300；`证据强度 中 · 15 / 45` 右）；section `padding:96px 128px 160px`。
  - 分隔页：`padding:96px 128px; justify-content:space-between`，260px 衬线数字（#244B74）+ 64px 章名，底部 事实/机制/判断 三栏（mono 标签 19px + 正文 23px）。
  - 关键数字页：4×2 格，数字 64px 衬线，标签写口径（估计/计算/调研/预测），页脚注明“口径不同，不可相加”。
  - 发现页：编号 + 一句结论 + 一行证据 + 强度标签；超过 5 条拆两页。
- 格式硬约束：内联样式闭合子集（px、hex；无渐变/阴影/z-index/em）；图片只用上传资产 `/_blob/<id>`；全出血底图放 section 第一个子元素，**其上的正文整体装进一个 `position:absolute;left:128px;top:96px;width:1664px;height:824px` 的容器**，否则会被底图盖住。
- 发布：`root` = 含 `project/` 的目录，`file_path` 一个文件，`files` 其余；改 deck.json 用 Edit；资产用 `asset:true` + `file_paths` 一次最多 25 个。

## 5. 风格样张（用户嫌“AI 感”时）
- 先做样张册再套全册：4 个方向 × 同 4 种页型（分隔/关键数字/图页/发现页），让用户横向比较。
  - A 暗室：dark.design、Linear/Vercel；#0B0D10 底 + #0F1217 面板 + #7AA2FF 强调，Space Grotesk 标题，JetBrains Mono 大写标签。
  - B 海报：recent.design、loadmo.re；#F2EFE6 底，Noto Serif SC 900 巨型数字，4px 黑线，整页朱红 #FF3B1F 陈述页（全册 ≤3 次）。
  - C 极简：minimal.gallery、瑞士网格；纯白，无线条，Space Grotesk 500，两级灰 #555/#8A8A8A，图表单色。
  - D 暖调：Typewolf 的 Daylight；杏 #F3E3C8 + 橄榄绿 #3F4A2E 左侧整栏色块，奶油 #FBF1DF 列表卡，中文数字序号。
- 背景手法（从 UI 设计借，静态可用；`decks/style_sampler/bg/gen_bg.py` 用 PIL 生成 1920×1080 底图）：E1 点阵网格+标尺刻度+裁切角标+幽灵数字（分隔页）；E2 节点连线图当底、标签用文字叠放（架构/产业链页）；E3 图表去字只留走势线、压到 40% 亮度（结论页，≤2 次）；E4 层叠窗口框：三层纯色块 + 1px 边线（图页）；E5 上下色块分割：上半一个数、下半四个口径（关键数字页）；E6 光晕+颗粒（暗底数字墙，JPEG 底图）。
- 用量原则：一页一种；全册背景手法 ≤3 种；背景对比度低于正文；Google 字体离线导出会回退，重度依赖的方向要说明。

### 补充文档
- `background-layers.md`：背景层 E1–E5 的落页规则、用量上限、生成与写法，以及套用到主 deck 的落位清单。E6 不采用。

## 6. 自查（用户允许时才做；做之前问一句）
- 本地 Chromium（Playwright）1920×1080 渲染每页：`tools/render/render.py`（主 deck）/ `render_s.py`（样张）；`blobmap.txt` 把 `/_blob/<id>` 映射到本地 PNG，字体用 Noto CJK 替代。
- 报告三类问题：正文触底（flowBottom ≥ 页脚 top−8）、元素越界/滚动溢出、标题 >2 行；全出血页触底属设计预期要单独说明。
- 拼 contact sheet 人眼复核孤字、换行；先列清单，改完再跑一次，只修清单上的问题。

## 交付话术
- 先说结果（页数、方向、未能做到的），再给一个下一步选择题（选哪个方向 / 哪些背景手法套全册）；不复述过程。
