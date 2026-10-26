set -e
cd /home/claude/report/build
python3 toc_gen.py init >/dev/null
for pass in 1 2 3; do
  node build2.js >/dev/null
  python3 post.py report_final.docx >/dev/null
  python3 /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf report_final.docx >/dev/null 2>&1
  python3 toc_gen.py fill report_final.pdf > /tmp/toc_$pass.txt
done
python3 -c "import pypdf;print('pages',len(pypdf.PdfReader('report_final.pdf').pages))"
python3 /tmp/claude-0/-home-claude/e9602583-6fd0-5070-905f-0a76d9c21e58/scratchpad/rowcheck.py report_final.docx report_final.pdf
diff -q /tmp/toc_2.txt /tmp/toc_3.txt && echo toc-stable
