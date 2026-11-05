# 方向 4 真实取证记录：贵州茅台（600519.SH）

本文记录用 `skill/management-topics.md` R1–R8 对贵州茅台跑一遍取证的过程与结论，供修订 skill 用。正文草稿在 `content/`。

## 1. 边界（R1）
- 对象：贵州茅台酒股份有限公司，合并报表口径；期间 FY2020–FY2024 年报 + 2025 年三季报。
- 同业对照组（≥3 家）：五粮液 000858、泸州老窖 000568、山西汾酒 600809。
- 读者：管理学课程 / 案例作业；输出：先出取证稿（content/），成片与否由用户决定。

## 2. 来源可达性（R5 的现实检验）
容器网络策略对所有一手与二手站点都拒绝（代理 CONNECT 403，WebFetch 报 DNS 不解析），只有 WebSearch 可用。探过的域名：

| 类别 | 域名 | 结果 |
|---|---|---|
| 交易所 / 披露平台 | www.sse.com.cn、static.sse.com.cn、query.sse.com.cn、www.szse.cn、www.cninfo.com.cn | 拒绝 |
| 公司官网 | www.moutaichina.com | 拒绝 |
| 公告 PDF 镜像 | pdf.dfcfw.com、data.eastmoney.com | 拒绝 |
| 统计与监管 | www.stats.gov.cn、data.stats.gov.cn、www.gov.cn | 拒绝 |
| 行业协会 | www.cada.cc | 拒绝 |
| 财经媒体 / 数据站 | finance.sina.com.cn、xueqiu.com、www.stcn.com、www.cs.com.cn、www.10jqka.com.cn、www.iwencai.com、www.sohu.com | 拒绝 |

**要放行的域名（按优先级）**：
1. 一手：`static.sse.com.cn`、`www.sse.com.cn`、`www.cninfo.com.cn`、`www.szse.cn`（同业三家在深交所）、`www.moutaichina.com`
2. 统计与行业：`www.stats.gov.cn`、`data.stats.gov.cn`、`www.cada.cc`
3. 公告 PDF 镜像（交易所站点慢或拦截自动抓取时的备选）：`pdf.dfcfw.com`

**降级口径**（主 skill §1）：所有数字都来自检索摘要，没有打开原文。因此：
- 任何数字不给「强」；
- ≥2 条独立检索线一致 → 「中」；
- 单一来源或机构间分歧 → 「弱」；
- 方法页写明限制；放行域名后对「中」的数字逐条开原文复核，可升「强」。

## 3. 规则检验（R1–R8）
（取证完成后填写）

## 4. 需要回写到 skill 的修订
（取证完成后填写）
