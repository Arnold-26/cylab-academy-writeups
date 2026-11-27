#!/bin/bash
cd . || exit 1
which nasm || exit 2
nasm -f bin -o _z_213sc.bin _z_213sc.asm || exit 3
python3 - <<'EOF'
d = open('./_z_213sc.bin','rb').read()
print("len:", len(d))
print("hex:", d.hex())
print("contient 0x0a:", b"\n" in d, "| 0x00:", b"\x00" in d)
EOF
