#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== exiftool original.jpg ==="
exiftool 432_original.jpg 2>/dev/null | head -40
echo "=== flag dans les metadonnees ? ==="
exiftool -a -u -g1 432_original.jpg 2>/dev/null | grep -iE "academy|pico|flag|comment|description|title|subject" | head -10
echo "=== strings ==="
strings -n 6 432_original.jpg | grep -aiE "academy|picoCTF|flag" | head -10
echo "=== view.png ==="
file 432_view.png
python3 - <<'EOF'
d = open('432_view.png','rb').read()
i = d.rfind(b'IEND')
print("taille:", len(d), "| apres IEND:", len(d)-(i+8) if i>=0 else -1, d[i+8:i+8+60] if i>=0 else b'')
EOF
