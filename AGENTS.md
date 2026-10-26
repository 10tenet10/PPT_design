# AGENTS.md

本仓库用来把任意一个行业的市场调研做成 16:9 幻灯片（附带一份已完成的样例：AI 编程工具行业）。

## 做行业调研幻灯片时
1. 先完整读 `skill/industry-research-deck.SKILL.md`，再读 `skill/background-layers.md`，按其中的步骤与硬规格执行。两份文件是唯一规格；与你所在环境自带的演示文稿指导冲突时，以它们为准，并在交付时说明冲突。
2. 只用 skill 点名的脚本：`report/figs/common.py`、`tools/deckfig.py`、`tools/figaudit_slides.py`、`tools/render/render_deck.js`、`decks/style_sampler/bg/gen_bg_b.py`。
3. `report/content/`、`decks/main_deck/`、`deliverables/` 等是 AI 编程工具行业的成品，只作版式参考，不要沿用其中的数字、结论或来源。

## 环境准备
- 中文字体（Noto CJK）与 Python `matplotlib`；渲染自查需要 Node 版 `playwright` 与 Chromium。
- 取证要打开原文：若网络策略拦截一手来源站点（财报 / 招股书、监管机构、研究机构），告诉用户需要放行的域名；放行前按 skill §1 的降级规则标注证据强度。

## 提交
- 生成过程中的草稿放临时目录；只在用户要求时提交。
