#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== chaines .rodata ==="
python3 - <<'EOF'
d = open('126_gauntlet','rb').read()
for a in (0x402004, 0x402008):
    off = a - 0x400000
    print(hex(a), repr(d[off:off+80].split(b'\x00')[0]))
EOF
echo "=== GNU_STACK ==="
readelf -lW 126_gauntlet 2>/dev/null | grep -A1 GNU_STACK
echo "=== verif offset : main utilise rbp-0x70 et ret a rbp+8 ==="
objdump -d -Mintel 126_gauntlet 2>/dev/null | sed -n '/<main>:/,/^$/p' | grep -E "lea.*0x70|strcpy|leave|ret"
