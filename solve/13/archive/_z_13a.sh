#!/bin/bash
cd /tmp/cylab_eps || exit 1
chmod +x 13_investigative-reversing-2-mystery 2>/dev/null
file 13_investigative-reversing-2-mystery | cut -c1-110
file 13_investigative-reversing-2-encoded.bmp
echo "=== symboles / chaines ==="
nm 13_investigative-reversing-2-mystery 2>/dev/null | grep -E " [Tt] " | head -8
strings -n 5 13_investigative-reversing-2-mystery | grep -aiE "flag|bmp|encoded|png|insert|found" | head -8
echo "=== BMP : octets apres la fin des donnees ? ==="
python3 - <<'EOF'
d = open('13_investigative-reversing-2-encoded.bmp','rb').read()
print("taille:", len(d), "| entete:", d[:2])
# taille BMP dans l entete (offset 2, 4 octets LE)
import struct
fsize = struct.unpack('<I', d[2:6])[0]
pixoff = struct.unpack('<I', d[10:14])[0]
print("fsize declare:", fsize, "| offset pixels:", pixoff, "| taille reelle:", len(d))
print("apres pixel data (si fsize < len):", d[fsize:fsize+120])
EOF
