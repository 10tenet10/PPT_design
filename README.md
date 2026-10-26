# PPT_design — 会话交接包

本仓库是「AI 编程工具行业分析报告 → 幻灯片版式设计」一次会话的全部工作文件，供云端任务继续。

## 当前状态（2026-10-26）
- 报告 v3（65 页 DOCX/PDF）已交付：`deliverables/`。
- 主幻灯片 45 页（编辑式视觉系统）已发布为 Slides 工件：https://claude.ai/artifact/（主 deck，见会话）。文件在 `decks/main_deck/project/`。
- 风格样张册 24 页已发布：https://claude.ai/artifact/GDqiKAbb6zF9sg2cBFjeYo 。文件在 `decks/style_sampler/project/`：
  - intro；A 暗室 a1–a4；B 海报 b1–b4；C 极简 c1–c4；D 暖调 d1–d4；E 背景元素实验 e0–e6。
- **待用户决定**：选哪个方向（A/B/C/D 或混搭）+ 哪些背景手法（E1–E6）套到 45 页主 deck。建议：E1 铺分隔页、E4 给图页、E5/E3 给 3–4 张结论页。
- 技能文本（待保存）：`skill/industry-research-deck.SKILL.md`；补充文档 `skill/background-layers.md`（背景层 E1–E5 落页与用量，已由用户确认采用）。

## 目录
- `report/content/` 报告正文（markdown 方言）；`report/build/build2.js` → DOCX（docx-js），`post.py`、`toc_gen.py`；`report/figs/` matplotlib 图脚本（`common.py` 统一风格）；`figs_deck/ figs_dark/ figs_mono/` 幻灯片版图。
- `decks/main_deck/project/` 主 deck（deck.json + slides/*.html）。
- `decks/style_sampler/project/` 样张册；`decks/style_sampler/bg/gen_bg.py` 生成背景底图（点阵、节点连线、曲线压暗、光晕颗粒、蓝图网格）。
- `tools/` 构建与自查脚本：`build.sh`、`rowcheck.py`（DOCX 表格行对 PDF 核对）、`figaudit*.py`、`figs_deck.py` + `deck_cfg.json`、`figs_variants.py`。
- `tools/render/` Playwright 渲染自查：`render.py`（主 deck）、`render_s.py`（样张册）、`blobmap.txt`（/_blob/<id> → 本地 PNG 映射）、两张 contact sheet。
- `source_post/` 用户给的帖子「硅谷设计师私藏的 10 个网站」正文与链接。

## 云端续作要点
- 幻灯片工件用 Artifact 工具发布：`root` = 含 `project/` 的目录，`file_path` 一个文件，`files` 其余；改 deck.json 用 Edit 不用 Write。
- 底图资产已上传到样张册（blob id 见 `tools/render/blobmap.txt` 末尾五行）；主 deck 若要用同样底图需重新上传到主 deck 工件。
- 幻灯片格式是内联样式闭合子集：无渐变/阴影/z-index；全出血底图上的正文须整体放进 `position:absolute` 容器。
- 渲染自查前需 `pip install playwright` 与本地 Chromium；中文字体用 Noto CJK 替代 Google 字体。
