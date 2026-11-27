#!/bin/bash
cd /tmp/cylab_eps || exit 1
OFF=731136
echo "=== istat inode 2365 (1.txt) ==="
istat -o $OFF 383_disk.img 2365 2>/dev/null | head -20
echo "=== contenu (12 octets attendus) ==="
icat -o $OFF 383_disk.img 2365 2>/dev/null | head -3
echo "=== slack : bloc complet ==="
python3 - <<'PYEOF'
import subprocess
out = subprocess.run(["istat","-o","731136","383_disk.img","2365"], capture_output=True, text=True).stdout
import re
blocks = re.findall(r"^\s*(\d+):\s*(\d+)$", out, re.M)
print("blocs:", blocks)
if blocks:
    blk = int(blocks[-1][0])
    print("dernier bloc:", blk)
    with open("383_disk.img","rb") as f:
        f.seek(731136*512 + blk*4096)
        data = f.read(4096)
    print("taille lue:", len(data))
    print("debut:", data[:60])
    tail = data[12:]
    nz = tail.rstrip(b"\x00")
    print("slack non nul:", len(nz))
    print("slack repr:", nz[:400])
PYEOF
