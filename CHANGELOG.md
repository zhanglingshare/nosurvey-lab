# Changelog

本项目遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [0.1.0] - 2026-10-05

### Added
- 五步工作流（构念解析 → 类型判定 → SRG 分级 → 数据源匹配 → 方案表输出）。
- SRG（问卷替代度）S/A/B/C/D 五级可引用标准（`references/srg-standard.md`）。
- 国内外双轨数据源地图、已验证代理清单、跨文化检查要点。
- 构念分级判定脚本 `scripts/grade_construct.py`（标准库可跑）。
- 标准交付模板 `templates/output-template.md`。
- 首个完整案例：国潮服饰购买意愿（S-O-R/SBC），含 16 件真实 SKU 的 GCS 客观编码、
  编码本、结构化数据、4 张可视化与双人信度工具（第三方原图不入库）。
