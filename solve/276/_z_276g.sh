#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== sections ==="
readelf -S 276_keygenme | grep -E '\.data|\.rodata|\.text|\.bss|rel'
echo "=== relocations ==="
readelf -r 276_keygenme 2>/dev/null | head -25
echo "=== hexdump 0x1200-0x1280 ==="
python3 - <<'EOF'
d = open("276_keygenme", "rb").read()
print(d[0x1200:0x1280])
EOF
