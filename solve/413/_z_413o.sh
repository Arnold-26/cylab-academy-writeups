#!/bin/bash
cd /tmp || exit 1
SRC=/tmp/cylab_eps/413_disk.flag.img.gz
echo "=== integrite du gz ==="
ls -la "$SRC"
gzip -t "$SRC" 2>&1 && echo "gz OK" || echo "gz CORROMPU/TRONQUE"
echo "=== taille attendue vs reelle ==="
python3 - <<'PYEOF'
import gzip, struct
src = "/tmp/cylab_eps/413_disk.flag.img.gz"
# la taille decompressee est dans les 4 derniers octets (ISIZE)
d = open(src,'rb').read()
print("ISIZE (mod 2^32):", struct.unpack('<I', d[-4:])[0])
PYEOF
echo "=== debugfs sur p3.img (erreurs incluses) ==="
debugfs -R "stats" p3.img 2>&1 | head -12
echo "=== stat inode 1333 ==="
debugfs -R "stat <1333>" p3.img 2>&1 | head -20
