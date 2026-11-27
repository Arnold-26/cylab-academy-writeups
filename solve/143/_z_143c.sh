#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== md5 ==="
md5sum 126_gauntlet 143_gauntlet
echo "=== chaines .rodata de 143 ==="
python3 - <<'EOF'
d = open('143_gauntlet','rb').read()
for a in (0x402004, 0x402008):
    off = a - 0x400000
    print(hex(a), repr(d[off:off+60].split(b'\x00')[0]))
EOF
echo "=== GNU_STACK 143 ==="
readelf -lW 143_gauntlet 2>/dev/null | grep GNU_STACK
echo "=== main 143 : printf et strcpy ==="
objdump -d -Mintel 143_gauntlet 2>/dev/null | sed -n '/<main>:/,/^$/p' | grep -E "lea|call|mov +esi|add +rax" | head -20
