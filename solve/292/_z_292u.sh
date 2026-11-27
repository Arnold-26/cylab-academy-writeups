#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
for A in 0x08093fd3 0x0804c325; do
  echo "=== octets a $A ==="
  python3 - "$A" <<'EOF'
import sys
a = int(sys.argv[1], 16)
d = open('292_vuln','rb').read()
OFF, VA = 0x1000, 0x08049000
i = OFF + (a - VA)
print("offset fichier:", hex(i), "octets:", d[i:i+12].hex())
EOF
  objdump -d -Mintel --start-address=$((A)) --stop-address=$((A+12)) 292_vuln 2>/dev/null | tail -8
done
