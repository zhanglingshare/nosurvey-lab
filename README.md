# No-Survey Lab · 问卷替代实验室

**Replace questionnaires with public data & digital traces — a decision engine for quantitative research.**
用公开数据、数字痕迹、行政记录与文本语料，替代问卷原本要拿的主观/行为数据；先判断“这个构念到底该不该发问卷”，再给可复现的取数方案。

[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/docs%20%26%20data-CC%20BY%204.0-lightgrey.svg)](LICENSE-DOCS.md)
[![Version](https://img.shields.io/badge/version-0.1.0-success.svg)](CHANGELOG.md)

### ▶ 在线试用（浏览器直接运行，无需安装）

**<https://zhanglingshare.github.io/nosurvey-lab/>** —— 打开后点“载入国潮案例 6 构念 → 开始判定”即可体验；纯前端、无后端、不上传数据。

## 为什么需要它

量化论文默认“数据＝问卷”，但问卷有三类内容，替代难度完全不同：

- **事实性自报**（收入、就业、消费）——客观存在，行政/统计/交易数据可直接替代；
- **行为性自报**（使用、参与、购买）——可被数字足迹观测，用真实行为替代自报；
- **心理性自报**（态度、感知、意图）——最难，用文本/痕迹代理 + 小样本校准。

> 问卷最大的浪费，是把**客观可观察的事实也拿去让人自报**。问卷不应是数据来源的默认项，而应是效度兜底项。

## 核心能力

1. 解析研究假设/概念图 → 结构化构念清单；
2. 判定测量类型（事实/行为/心理）；
3. **SRG 替代度分级**（S/A/B/C/D 五级，可引用标准）；
4. 匹配国内外数据源，给出 2–4 条测量路线；
5. 输出《问卷替代方案表》，附效度、合规与复现方式。

| 级别 | 含义 | 策略 |
|---|---|---|
| **S** | 直接替代（收入/就业/消费） | 全网替代，问卷不推荐 |
| **A** | 高度可替代（使用/参与） | 全网替代，问卷不推荐 |
| **B** | 可替代·需校准（态度/感知） | 替代为主 + 100–300 份效度锚点 |
| **C** | 部分替代·三角验证（深层心理） | 多源三角，问卷降级辅助 |
| **D** | 兜底（纯内在体验/私密行为） | 推荐行为实验任务替代自报 |

详见 [`references/srg-standard.md`](references/srg-standard.md)。

## 快速开始

**方式一：不依赖任何 Agent，直接跑脚本（Python 3）**

```bash
python3 scripts/grade_construct.py --construct "收入水平:事实" "使用强度:行为" "工作满意度:心理"
```

**方式二：作为 Agent Skill 安装**

```bash
bash install.sh
# 或指定目标目录： bash install.sh /path/to/skills/nosurvey-lab
```
安装后在支持 Skill 的助手中以“跑一个研究假设”触发，按 [`templates/output-template.md`](templates/output-template.md) 交付。

> 即使没有 Agent 运行时，`SKILL.md` 也是一份人可读的标准作业流程（SOP），脚本可独立运行。

## 仓库结构

```
SKILL.md              # Skill 入口 / 方法论 SOP
references/           # SRG 标准、数据源地图、已验证代理、跨文化检查
templates/            # 标准交付模板
scripts/              # 构念分级判定器（零依赖可跑）
examples/             # 真实案例（方法 + 结果，可复现）
```

## 示例：国潮服饰购买意愿（S-O-R / SBC）

对 16 件真实国潮 SKU 做 **GCS 客观编码**，把“文化刺激”从感知题还原为可观测产品特征：

![GCS 总分排序](examples/guochao-sbc/figures/fig1_total_rank.png)
![品类五维雷达](examples/guochao-sbc/figures/fig3_category_radar.png)

案例入口：[`examples/guochao-sbc/`](examples/guochao-sbc/README.md)。编码方法、结果与复现见
[`codebook.md`](examples/guochao-sbc/codebook.md) 与 [`coding-results.md`](examples/guochao-sbc/coding-results.md)。

## 引用

如用于论文或项目，请按 [`CITATION.cff`](CITATION.cff) 引用（提供 DOI 后更新于此）。

## 许可证

- **代码/脚本**：[MIT](LICENSE)
- **文档、方法论、数据（CSV）、图片（figures）**：[CC BY 4.0](LICENSE-DOCS.md)（署名即可）

## 第三方素材与合规

- SKU **原图受第三方版权保护，不随仓库分发**；仓库仅提供来源指针（[`sources.md`](examples/guochao-sbc/sources.md)）、编码后数据与统计图。
- 不提供受限平台（微博/小红书/抖音/知乎）的绕过/爬取方法；个人数据须去标识化与知情同意。详见各案例 `validity.md`。

## 贡献

欢迎贡献**验证案例、数据源更新与代理校验**，见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。
