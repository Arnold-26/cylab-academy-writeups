#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x400bb3 --stop-address=0x400c62 75_zero_to_hero 2>/dev/null | grep -vE "^$" | head -45
echo "=== chaines 0x400f0b .. 0x400f60 ==="
python3 - <<'EOF'
d = open('75_zero_to_hero','rb').read()
for a in (0x400f08, 0x400f0b, 0x400f0e, 0x400f20, 0x400f39, 0x400f40, 0x401040, 0x401043, 0x400ea6, 0x400ec0, 0x400ee0):
    off = a - 0x400000
    print(hex(a), repr(d[off:off+60].split(b'\x00')[0]))
EOF
