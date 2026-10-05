# SKU 原图目录（占位说明）

此目录用于存放国潮 SKU 原图，但这些图片来自第三方电商平台、**受版权保护，不随仓库分发**。

## 如何取得

按案例的来源登记 [`../../sources.md`](../../sources.md)，回到对应平台/店铺自行获取商品图，放入本目录，命名为 `sku-01.jpg … sku-16.jpg`。

## 不需要原图也能复现

仓库已提供：

- 编码后的结构化数据：[`../../data/gcs_coding.csv`](../../data/gcs_coding.csv)
- 由数据生成的统计图：[`../../figures/`](../../figures)
- 编码规则：[`../../codebook.md`](../../codebook.md)

获取原图后可运行：

```bash
cd ../..          # 进入 examples/guochao-sbc
python3 make_figures.py
python3 interrater_reliability.py
```
