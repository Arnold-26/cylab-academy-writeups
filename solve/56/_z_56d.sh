#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/b56 || exit 1
echo "=== signatures packaging ==="
strings main.exe | grep -aiE "pyinstaller|PYZ|MEI|python3|nuitka|py2exe|_MEIPASS" | head -10
echo "=== sections PE ==="
python3 - <<'EOF'
import struct
d = open('main.exe','rb').read()
pe = struct.unpack_from('<I', d, 0x3c)[0]
nsec = struct.unpack_from('<H', d, pe+6)[0]
opt = struct.unpack_from('<H', d, pe+20)[0]
base = pe + 24 + opt
print("sections:", nsec)
for i in range(nsec):
    o = base + i*40
    name = d[o:o+8].rstrip(b'\x00').decode(errors='replace')
    vsz, va, rsz, ro = struct.unpack_from('<IIII', d, o+8)
    print(f"  {name:10} va={va:#08x} vsz={vsz:8d} raw={rsz:8d}")
EOF
echo "=== binwalk rapide ==="
python3 - <<'EOF'
d = open('main.exe','rb').read()
for magic, label in ((b'PK\x03\x04','zip'), (b'\x1f\x8b','gzip'), (b'MZ','MZ'), (b'PYZ','PYZ')):
    i = d.find(magic)
    print(label, "offset", i if i>=0 else "-")
print("taille:", len(d))
EOF
