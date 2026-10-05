#!/usr/bin/env python3
"""双人编码信度（Inter-rater Reliability）
- 编码者A：data/gcs_coding.csv
- 编码者B：data/gcs_coding_b.csv
首次运行若B表缺失，生成空白模板 data/gcs_coding_b_blank.csv；第二编码者独立打分后
另存为 data/gcs_coding_b.csv 再运行。输出各维一致率、Cohen's kappa、总分 Pearson r。
"""
import os
import numpy as np
import pandas as pd

base = os.path.dirname(os.path.abspath(__file__))
datadir = os.path.join(base, "data")
A = pd.read_csv(os.path.join(datadir, "gcs_coding.csv"))
pathB = os.path.join(datadir, "gcs_coding_b.csv")
dims = ["M", "C", "S", "R", "D"]

if not os.path.exists(pathB):
    blank = A.copy()
    for c in dims + ["总分", "GCS指数", "强度"]:
        blank[c] = ""
    out = os.path.join(datadir, "gcs_coding_b_blank.csv")
    blank.to_csv(out, index=False)
    print("未发现编码者B表。已生成空白模板：", os.path.relpath(out, base))
    print("请第二编码者独立打分（勿看A结果），另存为 gcs_coding_b.csv 后重新运行。")
    raise SystemExit(0)

B = pd.read_csv(pathB)
m = A.merge(B, on="sku", suffixes=("_A", "_B"))
if m[[d + "_B" for d in dims]].isna().any().any():
    print("编码者B表存在未打分项，请补全后再运行。")
    raise SystemExit(1)


def cohen_kappa(x, y):
    x = np.asarray(x, dtype=int); y = np.asarray(y, dtype=int)
    cm = np.zeros((4, 4), dtype=float)
    for a, b in zip(x, y):
        cm[a, b] += 1
    n = cm.sum()
    po = np.trace(cm) / n
    pe = ((cm.sum(1) * cm.sum(0)).sum()) / (n ** 2)
    return (po - pe) / (1 - pe), po


print("维度  一致率  Cohen's kappa")
kappas = []
for d in dims:
    k, po = cohen_kappa(m[d + "_A"], m[d + "_B"])
    kappas.append(k)
    print(f"{d}     {po:.3f}   {k:.3f}")
print("各维 kappa 均值: %.3f" % np.mean(kappas))
print("总分 Pearson r = %.3f" % np.corrcoef(m["总分_A"], m["总分_B"])[0, 1])
print("B−A 总分平均偏差 = %.2f" % (m["总分_B"] - m["总分_A"]).mean())
print("判读：kappa ≥0.75 良好，0.60–0.74 可接受，<0.60 需修订编码本/重新培训。")
