#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x4008e7 --stop-address=0x4009a0 55_sice_cream 2>/dev/null | grep -vE "^$" | head -30
echo "=== chaines autour de 0x400f10 ==="
python3 - <<'EOF'
d = open('55_sice_cream','rb').read()
for a in (0x400ee8, 0x400f10, 0x400f3a, 0x400e21, 0x400e40, 0x400e4d):
    off = a - 0x400000
    print(hex(a), repr(d[off:off+60].split(b'\x00')[0]))
EOF
