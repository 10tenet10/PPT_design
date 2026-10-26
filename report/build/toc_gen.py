"""TOC page numbers from the PDF outline (exact). usage: toc_gen.py init | toc_gen.py fill <pdf>"""
import re, json, sys, os
ROOT = "/home/claude/report"
FILES = ["00_front.md", "01_ch1.md", "02_ch2.md", "03_ch3.md", "04_ch4.md", "05_ch5.md", "06_ch6.md", "07_ch7.md", "08_ch8.md", "refs.md", "09_appendix.md"]
heads = []
for f in FILES:
    for L in open(os.path.join(ROOT, "content", f), encoding="utf8"):
        if L.startswith("# "): heads.append((1, L[2:].strip()))
        elif L.startswith("## "): heads.append((2, L[3:].strip()))
out = f"{ROOT}/build/toc_pages.json"
if sys.argv[1] == "init":
    json.dump({"entries": [{"level": l, "text": t, "page": "00"} for l, t in heads]}, open(out, "w"), ensure_ascii=False)
    print("init", len(heads))
else:
    import pypdf
    r = pypdf.PdfReader(sys.argv[2])
    found = {}
    def walk(o):
        for it in o:
            if isinstance(it, list): walk(it)
            else:
                t = re.sub(r"\s+", " ", it.title).strip()
                found.setdefault(t, r.get_destination_page_number(it) + 1)
    walk(r.outline)
    entries = []
    for l, t in heads:
        key = re.sub(r"\s+", " ", t).strip()
        if key not in found: print("MISSING", t)
        entries.append({"level": l, "text": t, "page": str(found.get(key, "?"))})
    json.dump({"entries": entries}, open(out, "w"), ensure_ascii=False)
    print("\n".join(f"{e['page']:>3} {'  ' * (e['level'] - 1)}{e['text']}" for e in entries))

    # exhibit pages: find line starting with label + start of title
    import subprocess
    ex = json.load(open(f"{ROOT}/build/exhibits.json"))
    n = len(r.pages)
    pages = []
    for p in range(1, n + 1):
        txt = subprocess.check_output(["pdftotext", "-f", str(p), "-l", str(p), "-raw", sys.argv[2], "-"]).decode("utf8")
        pages.append(re.sub(r"\s+", "", txt))
    first_body = min(int(e["page"]) for e in entries if e["text"].startswith("第一章"))
    res = {}
    for e in ex:
        key = re.sub(r"\s+", "", e["label"] + e["title"][:8])
        for p in range(first_body, n + 1):
            if key in pages[p - 1]:
                res[e["label"]] = p; break
        else:
            print("EXHIBIT MISSING", e["label"])
    json.dump(res, open(f"{ROOT}/build/exhibit_pages.json", "w"), ensure_ascii=False)
    print("exhibits", len(res), "/", len(ex))
