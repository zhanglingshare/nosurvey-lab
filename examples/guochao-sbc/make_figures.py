#!/usr/bin/env python3
"""GCS 客观编码结果可视化（可复现）
读 data/gcs_coding.csv，输出 figures/*.png，并打印描述统计。
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Patch

cand = ["Noto Sans CJK SC", "Noto Sans CJK HK", "Droid Sans Fallback", "AR PL UMing CN"]
avail = {f.name for f in fm.fontManager.ttflist}
fname = next((c for c in cand if c in avail), "Droid Sans Fallback")
plt.rcParams["font.sans-serif"] = [fname]
plt.rcParams["axes.unicode_minus"] = False

base = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(base, "data", "gcs_coding.csv"))
outdir = os.path.join(base, "figures")
os.makedirs(outdir, exist_ok=True)

dims = ["M", "C", "S", "R", "D"]
dimlabels = ["传统纹样", "传统工艺", "传统版型", "当代重构", "元素密度"]
catcolor = {"裙装": "#C0392B", "外套": "#D68910", "T恤": "#1F8A70",
            "卫衣": "#2E86C1", "裤装": "#7D8517"}
dimcolors = ["#C0392B", "#E67E22", "#E8B50D", "#16A085", "#2E86C1"]

d = df.sort_values("总分")
fig, ax = plt.subplots(figsize=(9, 7))
ax.barh(d["sku"], d["总分"], color=d["品类"].map(catcolor))
for i, v in enumerate(d["总分"]):
    ax.text(v + 0.15, i, str(v), va="center", fontsize=9)
ax.set_xlim(0, 15)
ax.set_xlabel("GCS 总分（0–15）")
ax.set_title("16 件国潮 SKU · GCS 客观编码总分排序")
present = [k for k in catcolor if k in set(df["品类"])]
ax.legend(handles=[Patch(color=catcolor[k], label=k) for k in present],
          loc="lower right", title="品类")
fig.tight_layout(); fig.savefig(os.path.join(outdir, "fig1_total_rank.png"), dpi=150); plt.close(fig)

d = df.sort_values("总分")
fig, ax = plt.subplots(figsize=(10, 6.5))
left = np.zeros(len(d))
for k, dim in enumerate(dims):
    ax.barh(d["sku"], d[dim], left=left, color=dimcolors[k], label=dimlabels[k])
    left += d[dim].values
ax.set_xlim(0, 15)
ax.set_xlabel("GCS 总分（五维堆叠）")
ax.set_title("GCS 五维度构成（按总分排序）")
ax.legend(ncol=5, loc="lower right", fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(outdir, "fig2_dim_stack.png"), dpi=150); plt.close(fig)

cats = ["裙装", "外套", "卫衣", "T恤", "裤装"]
g = df.groupby("品类")[dims].mean().reindex(cats)
ang = np.linspace(0, 2 * np.pi, len(dims), endpoint=False).tolist(); ang += ang[:1]
fig = plt.figure(figsize=(8.6, 7)); ax = plt.subplot(111, polar=True)
for cat in cats:
    vals = g.loc[cat].tolist(); vals += vals[:1]
    ax.plot(ang, vals, color=catcolor[cat], label=cat, linewidth=2)
    ax.fill(ang, vals, color=catcolor[cat], alpha=0.06)
ax.set_xticks(ang[:-1]); ax.set_xticklabels(dimlabels)
ax.set_ylim(0, 3)
ax.set_title("各品类 GCS 五维均值轮廓", pad=22)
ax.legend(loc="upper right", bbox_to_anchor=(1.32, 1.12))
fig.tight_layout(); fig.savefig(os.path.join(outdir, "fig3_category_radar.png"), dpi=150); plt.close(fig)

picks = [("sku-14 酒红妆花马面裙（总分14）", "sku-14"),
         ("sku-02 青花瓷满印T恤（11）", "sku-02"),
         ("sku-13 红羊羔绒盘扣外套（9）", "sku-13"),
         ("sku-15 黑底白描山水马面裙（8）", "sku-15")]
fig, axes = plt.subplots(2, 2, figsize=(10, 9), subplot_kw=dict(polar=True))
for ax, (label, sku) in zip(axes.ravel(), picks):
    row = df[df["sku"] == sku].iloc[0]
    vals = [row[x] for x in dims]; vals += vals[:1]
    ax.plot(ang, vals, color=catcolor[row["品类"]], linewidth=2)
    ax.fill(ang, vals, color=catcolor[row["品类"]], alpha=0.12)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(dimlabels, fontsize=8)
    ax.set_ylim(0, 3); ax.set_title(label, fontsize=10, pad=14)
fig.suptitle("代表性 SKU 的 GCS 五维轮廓", fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.97])
fig.savefig(os.path.join(outdir, "fig4_example_radar.png"), dpi=150); plt.close(fig)

print("样本量 n =", len(df))
print("总分: 均值%.2f 中位%.1f 范围%d–%d" % (
    df["总分"].mean(), df["总分"].median(), df["总分"].min(), df["总分"].max()))
print("各维均值:", {dl: round(float(df[d_].mean()), 2) for d_, dl in zip(dims, dimlabels)})
print("强度分布:", df["强度"].value_counts().to_dict())
print("品类均分:\n", df.groupby("品类")["总分"].mean().round(2).to_string())
print("已生成图:", sorted(os.listdir(outdir)))
