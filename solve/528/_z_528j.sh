#!/bin/bash
cd /tmp/cylab_eps || exit 1
F=m528/528_minions/res/drawable/minion.jpg
ls -la "$F"
echo "=== exiftool ==="
exiftool "$F" 2>/dev/null | head -25
echo "=== strings ==="
strings -n 5 "$F" | head -20
echo "=== donnees apres EOI (FFD9) ==="
python3 - <<'EOF'
d = open('/tmp/cylab_eps/m528/528_minions/res/drawable/minion.jpg','rb').read()
print("taille:", len(d), "| debut:", d[:4].hex())
i = d.rfind(b'\xff\xd9')
print("EOI a:", i, "| octets apres:", len(d) - i - 2)
if len(d) - i - 2 > 0:
    print("apres EOI:", d[i+2:i+2+200])
# commentaires COM (FFFE)
j = 2
while j < len(d) - 1:
    if d[j] != 0xFF:
        j += 1
        continue
    m = d[j+1]
    if m == 0xFE:
        ln = int.from_bytes(d[j+2:j+4], 'big')
        print("COM segment:", d[j+4:j+2+ln][:200])
    j += 1
EOF
