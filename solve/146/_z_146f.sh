#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== chaines .rodata ==="
python3 - <<'EOF'
d = open('146_heapedit','rb').read()
# .rodata ~ 0x400b00 -> file offset 0xb00
for addr in (0x400b08, 0x400b0a, 0x400b18, 0x400b3e, 0x400b48, 0x400b4b, 0x400b53):
    off = addr - 0x400000
    s = d[off:off+40].split(b'\x00')[0]
    print(hex(addr), repr(s))
EOF
