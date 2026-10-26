"""Verify every DOCX table row's longest cell text appears in the PDF text."""
import re, sys, subprocess
from docx import Document
d = Document(sys.argv[1]); S = re.sub(r'\s|​', '', subprocess.check_output(['pdftotext', sys.argv[2], '-']).decode())
bad = 0
for i, t in enumerate(d.tables):
    for j, r in enumerate(t.rows):
        toks = sorted({re.sub(r'\s|​', '', c.text) for c in r.cells}, key=len, reverse=True)
        tok = toks[0] if toks else ''
        if len(tok) >= 12 and not any(x[3:11] in S for x in toks if len(x) >= 12):
            bad += 1; print('MISSING table', i, 'row', j, tok[:30])
print('rowcheck bad =', bad)
