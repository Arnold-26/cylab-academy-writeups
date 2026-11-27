#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== /root ==="
fls -p 87_suspicious.dd.sda1 2009 2>/dev/null | head -5
fls -r -p 87_suspicious.dd.sda1 2>/dev/null | grep -iE "root|flag|secret|\.txt" | head -15
echo "=== blocs de l'inode 12 ==="
istat 87_suspicious.dd.sda1 12 2>/dev/null | grep -A3 "Direct Blocks"
echo "=== slack (bloc complet) ==="
python3 - <<'EOF'
import subprocess, re
out = subprocess.run(["istat", "87_suspicious.dd.sda1", "12"], capture_output=True, text=True).stdout
m = re.search(r"Direct Blocks:\s*\n\s*(\d+)", out)
print("istat:", out[-200:])
if m:
    blk = int(m.group(1))
    with open("87_suspicious.dd.sda1", "rb") as f:
        f.seek(blk * 1024)
        data = f.read(1024)
    print("bloc", blk, "taille lue", len(data))
    print("contenu:", data[:200])
    print("slack apres 55:", data[55:400])
EOF
