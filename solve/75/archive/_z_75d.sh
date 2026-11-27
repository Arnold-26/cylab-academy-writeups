#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x400d3c --stop-address=0x400de0 75_zero_to_hero 2>/dev/null | grep -vE "^$"
echo "=== chaines utilisees ==="
python3 - <<'EOF'
d = open('75_zero_to_hero','rb').read()
for a in (0x400f75, 0x400f87, 0x400fa2, 0x400fc0, 0x400ff0, 0x400e9b, 0x400e9d):
    off = a - 0x400000
    print(hex(a), repr(d[off:off+80].split(b'\x00')[0]))
EOF
