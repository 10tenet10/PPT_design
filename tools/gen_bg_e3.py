"""E3 底图（通用）：走势线只占右上区域，线色 = 正文色相对亮度的 40%，无字、不淡出。
用法：python3 tools/gen_bg_e3.py <spec.json> <out.png>
spec 字段：
  bg      底色（编辑式 #0B0D10；B 海报 #111111）
  text    该页正文色（编辑式 #E8EAEE；B 海报 #F2EFE6），线色由它按相对亮度 ×0.4 算出
  grid    基线色（比底色亮一档，如 #1E2630）
  xlim / ylim   数据范围；纵轴从 0 起
  series  [{"x": [...], "y": [...], "dash": false, "lw": 5, "ms": 13}]  原始数据点
  marks   {"名称": [x, y]}  需要 HTML 标签的点（端点、年份基线等）
输出：PNG，以及打印每个 mark 在 1920×1080 画布上的像素坐标，供 HTML 标签定位。"""
import sys, json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REGION = (1000, 1760, 150, 520)  # x0, x1, y0, y1（像素）：右上区域，避开左下的大数字与标题


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _srgb(v):
    return round(255 * (12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055))


def line_color(text_hex, ratio=0.4):
    """保持正文色相，在线性空间等比缩放，使相对亮度 = 正文 × ratio。"""
    rgb = [_lin(int(text_hex[i:i + 2], 16)) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(_srgb(c * ratio) for c in rgb)


def main(spec_path, out):
    s = json.load(open(spec_path))
    x0, x1, y0, y1 = REGION
    ln = line_color(s["text"])
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor=s["bg"])
    ax = fig.add_axes([x0 / 1920, 1 - y1 / 1080, (x1 - x0) / 1920, (y1 - y0) / 1080], facecolor=s["bg"])
    ax.set_xlim(*s["xlim"]); ax.set_ylim(*s["ylim"]); ax.axis("off")
    ax.plot(s["xlim"], [0, 0], color=s.get("grid", "#1E2630"), lw=2, clip_on=False)
    for se in s["series"]:
        ax.plot(se["x"], se["y"], "--o" if se.get("dash") else "-o", color=ln, lw=se.get("lw", 5), ms=se.get("ms", 12))
    fig.canvas.draw()
    pts = {}
    for k, (x, y) in s.get("marks", {}).items():
        X, Y = ax.transData.transform((x, y)); pts[k] = [round(X), round(1080 - Y)]
    fig.savefig(out, facecolor=s["bg"]); plt.close(fig)
    print(json.dumps({"line_color": ln, "marks": pts}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
