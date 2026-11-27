#!/bin/bash
# 27 - Investigative Reversing 1  (Forensics, picoCTF 2019)
# Flag: academy{An0tha_1_1730fa2f}
# Write-up: ../../../writeups/forensics/27-investigative-reversing-1.md
# Script exact utilise pour produire le flag.
#
cd /tmp/cylab_eps || exit 1
chmod +x 27_investigative-reversing-1-mystery 2>/dev/null
echo "=== images : taille et octets apres IEND ==="
for F in 27_investigative-reversing-1-mystery.png 27_investigative-reversing-1-mystery2.png 27_investigative-reversing-1-mystery3.png; do
  [ -f "$F" ] || continue
  python3 - "$F" <<'EOF'
import sys
p = sys.argv[1]
d = open(p,'rb').read()
i = d.rfind(b'IEND')
print("%-40s taille=%-8d apres_IEND=%d %r" % (p, len(d), len(d)-(i+8) if i>=0 else -1, d[i+8:i+8+60] if i>=0 else b''))
EOF
done
echo "=== binaire : chaines ==="
strings -n 4 27_investigative-reversing-1-mystery | grep -aiE "flag|png|mystery|insert|found" | head -10
echo "=== binaire : main (extrait) ==="
objdump -d -Mintel 27_investigative-reversing-1-mystery 2>/dev/null | sed -n '/<main>:/,/^$/p' | grep -E "fputc|add|sub|xor|fread|fopen|movzx|cmp|lea.*rip" | head -40
