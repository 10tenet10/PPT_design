"""把 export_deck.js 的逐页截图与讲稿拼成 16:9 PPTX（每页一张全幅图片 + 讲稿备注）。
页面是图片，不可编辑文字；要可编辑版本，请在 Slides 工件页面用 Share › Export 导出 PPTX。
用法：python3 tools/render/pptx_from_png.py <输出路径前缀> <标题>
"""
import io, json, sys, glob
from PIL import Image
from pptx import Presentation
from pptx.util import Emu

prefix, title = sys.argv[1], sys.argv[2]
prs = Presentation()
prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)   # 13.333 × 7.5 in
prs.core_properties.title = title
blank = prs.slide_layouts[6]
notes = json.load(open(prefix + "_notes.json", encoding="utf-8"))
pngs = sorted(glob.glob(prefix + "_png/*.png"))
assert len(pngs) == len(notes), (len(pngs), len(notes))
for png, n in zip(pngs, notes):
    s = prs.slides.add_slide(blank)
    buf = io.BytesIO()   # 截图转 JPEG 嵌入，体积约为 PNG 的一半
    Image.open(png).convert("RGB").save(buf, "JPEG", quality=90, optimize=True); buf.seek(0)
    s.shapes.add_picture(buf, 0, 0, width=prs.slide_width, height=prs.slide_height)
    if n["notes"]:
        s.notes_slide.notes_text_frame.text = n["notes"]
prs.save(prefix + ".pptx")
print("saved", prefix + ".pptx", len(pngs), "slides")
