#!/bin/bash
echo "=== outils forensics ==="
for t in fls mmls icat fsstat tsk_recover volatility3 vol.py foremost binwalk; do printf "%-14s " "$t"; which $t 2>/dev/null || echo "(absent)"; done
echo
ls -la ~/Downloads/partition4.img ~/Downloads/timeline-1-partition4.img.gz 2>/dev/null
echo "=== type du fichier ==="
file ~/Downloads/partition4.img 2>/dev/null | cut -c1-160
echo "=== fsstat ==="
fsstat ~/Downloads/partition4.img 2>&1 | head -15
