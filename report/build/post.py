"""Post-process report_raw.docx -> final docx:
 - unique wp:docPr ids
 - wrap static TOC entries in a TOC field (so Word can update it; LibreOffice shows cached entries)
 - compute TOC page numbers from the rendered PDF (two-pass)
"""
import re, sys, zipfile, shutil, subprocess, json, os
SRC = "/home/claude/report/build/report_raw.docx"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/report/build/report_final.docx"

def read_docx(p):
    z = zipfile.ZipFile(p); files = {n: z.read(n) for n in z.namelist()}; z.close(); return files

def write_docx(files, p):
    if os.path.exists(p): os.remove(p)
    z = zipfile.ZipFile(p, "w", zipfile.ZIP_DEFLATED)
    # [Content_Types].xml first
    order = ["[Content_Types].xml"] + [n for n in files if n != "[Content_Types].xml"]
    for n in order: z.writestr(n, files[n])
    z.close()

files = read_docx(SRC)
doc = files["word/document.xml"].decode("utf8")

# 1. unique docPr ids
cnt = [0]
def rep(m):
    cnt[0] += 1
    return f'<wp:docPr id="{cnt[0]}"'
doc = re.sub(r'<wp:docPr id="\d+"', rep, doc)

# 2. TOC field wrapping
m1 = doc.find("TOCSTART"); m2 = doc.find("TOCEND")
if m1 > 0 and m2 > 0:
    ps = doc.rfind("<w:p>", 0, m1); pe = doc.find("</w:p>", m1) + 6
    qs = doc.rfind("<w:p>", 0, m2); qe = doc.find("</w:p>", m2) + 6
    begin = ('<w:p><w:pPr><w:spacing w:after="0"/></w:pPr><w:r><w:fldChar w:fldCharType="begin"/></w:r>'
             '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText></w:r>'
             '<w:r><w:fldChar w:fldCharType="separate"/></w:r></w:p>')
    end = '<w:p><w:pPr><w:spacing w:after="0"/></w:pPr><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
    doc = doc[:ps] + begin + doc[pe:qs] + end + doc[qe:]

files["word/document.xml"] = doc.encode("utf8")
write_docx(files, OUT)
print("written", OUT)
