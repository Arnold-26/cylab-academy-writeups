#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== appels fopen ==="
objdump -d -Mintel 55_sice_cream 2>/dev/null | grep -B12 "call.*<fopen@plt>" | head -30
echo "=== chaines du .rodata (toutes) ==="
python3 - <<'EOF'
import subprocess
out = subprocess.run(["readelf","-x",".rodata","55_sice_cream"], capture_output=True, text=True).stdout
import re
print(out[:1200])
EOF
