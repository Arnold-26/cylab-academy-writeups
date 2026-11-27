#!/bin/bash
cd /tmp/cylab_bin || exit 1
echo "=== offsets libc ==="
python3 - <<'EOF'
import subprocess, re
libc = "449_libc.so.6"
out = subprocess.run(["readelf", "-sW", libc], capture_output=True, text=True).stdout
for line in out.splitlines():
    p = line.split()
    if len(p) >= 8 and p[7] in ("system", "setvbuf", "puts", "printf"):
        print(p[7], p[1], p[2])
EOF
