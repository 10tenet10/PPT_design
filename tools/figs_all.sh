cd /home/claude/report/figs && for f in make_figs_a.py make_figs_a_fix.py make_figs_b.py make_figs_c.py; do python3 $f >/dev/null || echo FAIL $f; done; echo figs-done
