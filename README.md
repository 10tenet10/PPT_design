# PPT_design — 行业调研幻灯片 skill 与样例

本仓库提供一个把任意行业调研做成 16:9 幻灯片的 skill（`skill/`），附一份完整样例：AI 编程工具行业报告与幻灯片。

## 新行业从这里开始
- 一句话提示（任何编码智能体通用）：
  > 先完整阅读本仓库的 `skill/industry-research-deck.SKILL.md` 与 `skill/background-layers.md` 并严格照做，就〈行业名〉做一份行业调研幻灯片。
- 入口文件：`AGENTS.md`（Codex 等读取）、`CLAUDE.md`（Claude Code，导入 AGENTS.md）；不读这两个文件的工具，用上面那句提示即可。
- 两份 skill 文件是唯一规格：`industry-research-deck.SKILL.md` 管取证、图表、成片与自查；`background-layers.md` 管背景层 E1–E5 的参数、生成与落位。
- 环境准备：中文字体 Noto CJK、Python `matplotlib`；渲染与字号填充需 Node 版 `playwright` + Chromium。取证需要能打开一手来源站点，被网络策略拦截时在环境设置里放行。

### 新行业可用的工具
| 用途 | 文件 |
|---|---|
| 图表统一风格 | `report/figs/common.py`（被下一行导入） |
| 幻灯片版作图层 | `tools/deckfig.py`；范例 `tools/examples/smart_ring_make_figs.py` |
| 图表审计（重叠、溢出、小字） | `tools/figaudit_slides.py` |
| 背景层底图 | `decks/style_sampler/bg/gen_bg_b.py`（E1、E2）；`tools/gen_bg_e3.py`（E3，范例 `tools/examples/smart_ring_e3_pred.json`） |
| 成片字号填充 | `tools/render/fit_text.js` |
| 渲染自查 | `tools/render/render_deck.js` |

成片后的顺序：先 `node tools/render/fit_text.js <project 目录> <blobmap>` 把字号抬到基准并按空间放大，再 `node tools/render/render_deck.js <project 目录> <blobmap> <输出目录>` 渲染自查。blobmap 把幻灯片里的 `/_blob/<id>` 映射到本地 PNG（每行“id 路径”，或 JSON）。

## 样例：AI 编程工具行业
样例只作版式与流程参考，不要沿用其中的数字、结论与来源。

### 内容
- **报告**：`deliverables/` 下三版 DOCX/PDF（最新为 v3，65 页）；正文在 `report/content/`（markdown 方言），图表脚本与成图在 `report/figs/`，幻灯片版图在 `report/figs_deck/`、`figs_dark/`、`figs_mono/`。
- **主幻灯片**：`decks/main_deck/project/`（`deck.json` + 47 个 `slides/*.html`），B 海报方向 + 背景层 E1–E5；底图在 `decks/main_deck/bg/`，编辑式改 B 海报的转换脚本 `decks/main_deck/to_b.py`。改版前的编辑式 45 页见 git 历史。
- **风格样张册**：`decks/style_sampler/project/`，24 页：intro；A 暗室 a1–a4；B 海报 b1–b4；C 极简 c1–c4；D 暖调 d1–d4；E 背景元素实验 e0–e6。底图脚本 `decks/style_sampler/bg/gen_bg.py`、`gen_bg_b.py`。
- **参考来源**：`source_post/` 是用户给的帖子「硅谷设计师私藏的 10 个网站」正文与链接，样张册的四个方向取材于此。

### 本地预览
幻灯片文件是 Slides 工件格式（内联样式 HTML），图片引用 `/_blob/<id>`。在仓库根目录运行即可在本地看成片：

```
node tools/render/render_deck.js decks/main_deck/project tools/render/blobmap.txt out/main_deck
node tools/render/render_deck.js decks/style_sampler/project tools/render/blobmap.txt out/style_sampler
```

`tools/render/blobmap.txt` 用仓库内相对路径；输出每页一张 1920×1080 PNG 和一份 `report.json`。

`tools/rowcheck.py`（DOCX 表格行对 PDF 核对，参数为两个文件路径）不依赖固定路径，需要 DOCX/PDF 报告时可用。
