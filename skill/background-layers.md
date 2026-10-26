# 补充文档：背景层（E1–E5）落页规则与用量原则

本文是 `industry-research-deck` 的补充，规定主 deck 使用的五种静态背景层、各自落在哪类页面、全册用量上限，以及生成与写法。E6（光晕+颗粒）不采用。

## 为什么是静态层
幻灯片没有动效和滚动；UI 设计里让页面「不空」的大多是静态层。幻灯片格式只收纯色（无渐变/阴影），因此底图一律做成 PNG/JPEG 资产上传（`/_blob/<id>`），导出 PPTX 时原样保留。

## 五种背景层 → 页面类型

| 编号 | 手法 | 来源 | 落在哪类页 | 全册用量 |
|---|---|---|---|---|
| E1 | 点阵网格 + 左侧标尺刻度 + 四角裁切标记 + 幽灵章节数字 | Linear / Vercel 文档页 | **所有章节分隔页**（8 页）与封面 | 分隔页全铺；其他页不用 |
| E2 | 节点连线示意图当底，标签用文字叠在节点下 | Mobbin MCP 海报 | **架构 / 产业链 / 生态关系页**（如 s4-chain、s6-arch） | ≤3 页；用了 E2 的页不再放架构图 |
| E3 | 图表去坐标去文字、只留走势线、压到 ~40% 亮度，大字结论压在上面 | Godly 上 Ascension 式全出血页 | **章节结论页 / 一句话结论页**（如 s2-arr 之前加一页「40×」） | ≤2 页；真正的数据图放在相邻页正常展示 |
| E4 | 层叠窗口框：图表装进带标题栏的窗口，后面两层错位空框 | Mobbin 的 B150 截图 | **所有图页**（图 + 一句话结论的页型） | 图页全用；三层均为纯色块 + 1px 边线，不用阴影 |
| E5 | 上下色块分割：上半块一个数，下半块四个口径 | Godly 上 KIM 海报 | **关键数字页 / 执行摘要统帅页**（stats、各章首个关键数字页） | ≤3 页；朱红/强调色只在此类页出现 |

落页优先级（同一页多种手法冲突时）：E5 > E3 > E2 > E4 > E1。一页只能有一种。

## 用量原则（硬性）
1. 一页只用一种背景手法。
2. 全册背景手法不超过三种的**同时出现在相邻 5 页内**；整册五种都可用，但要按上表的页型分配，不混用。
3. 任何背景元素的对比度低于正文：纸色底上背景线/点 ≤ #D9D4C8，暗底上 ≤ #1E2630；幽灵数字 ≤ #E7E2D6。
4. 底图不带任何文字（E2 的标签是 HTML 文字叠放，不画进图里）。
5. 超过上述用量即回到「AI 模板感」；宁可留白也不叠第二层。

## 生成
- 脚本：`decks/style_sampler/bg/gen_bg.py`（PIL + numpy，1920×1080）。E1 `bg_dotgrid.png`（~10 KB）、E2 `bg_network.png`（~12 KB，节点坐标：hub (1380,540)，节点 (1040,300/540/780)、(1700,330/540/750)、(1380,220/860)）、E3 `bg_chartfade.png`（合成三条走势线 + 高斯光晕，再整体压暗，~75 KB）。
- E4、E5 不用底图，纯 div 实现（见下）。
- 用 Artifact `asset:true` + `file_paths` 一次上传；把返回的 id 记进 `tools/render/blobmap.txt` 供本地渲染。

## 写法（幻灯片格式子集内）
- **E1 / E2 / E3（全出血底图页）**：`<img src="/_blob/<id>" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover">` 作 section 第一个子元素；section 本身不设 padding；**正文整体装进一个 `position:absolute;left:128px;top:96px;width:1664px;height:824px;display:flex;flex-direction:column` 的容器**（分隔页 top:128px;height:792px），页脚仍是 `bottom:64px` 的 pinned 行。不这样做，正文会被底图盖住。
- **E2 标签**：每个节点一条 `position:absolute` 的 mono 20px 文字，`left = 节点x−80, top = 节点y+52, width:160px;text-align:center`；hub 标签 22px 粗体。
- **E3 文字区**：大数 200px Noto Serif SC 900 + 48px 标题 + 两栏 22px 说明，整体落在底图左下已压暗的区域（宽 ≤1100px）。
- **E4 窗口**：三个 `position:absolute` 的 div，依次 `left:744/776/808px; top:150/186/222px; width:1040px; height:720px; border-radius:14px; border:1px solid #D6D2C8`，底色 #ECE8DD / #F2EEE5 / #FFFFFF；前窗内：48px 标题栏（三个 12px 圆点 + mono 18px 文件名/样本量）+ `<img 1000×600 contain>`；左侧 540px 文字栏放标题（40px）+ 一句说明 + 3–4 行关键数。
- **E5 分割**：section `padding:0; flex-direction:column`；上块 `height:560px; background:#FF3B1F`（或主色 #244B74）内放 300px 巨数 + 右侧 28px 说明；下块 `flex:1` 内 4 栏，每栏 `border-top:3px solid #1A1D22`，mono 18px 口径标签 + 64px 数字 + 20px 说明；页脚注明「口径不同，不可相加」。

## 套用到 45 页主 deck 的落位清单
- E1：d1–d8 共 8 页分隔页 + cover。
- E4：s1-map、s2-timeline、s2-sources、s2-forecast、s2-bottomup、s2-arr、s2-china、s2-trust、s3-prices、s3-swebench、s4-value、s5-segments、s5-qa、s5-journey、s6-memory、s6-horizon、s7-usage、s7-forces、s7-pricing、s8-risk 等所有「标题 + 图」页。
- E2：s4-chain、s6-arch（≤3 页，连线图替代原架构图或与之并存时只留一个）。
- E5：stats（执行摘要关键数字页）；可另选 1–2 页章内关键数字页。
- E3：在 s2-arr 之前或 s8-predictions 之前各加 1 页一句话结论页，≤2 页。
- 自查：套用后跑 `tools/render/render.py`，全出血页触底为设计预期，其余照常。
