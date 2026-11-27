#!/bin/bash
cd . || exit 1
nasm -f bin -o _z_213sc2.bin _z_213sc2.asm || exit 3
python3 - <<'EOF'
d = open('./_z_213sc2.bin','rb').read()
print("len:", len(d))
print("hex:", d.hex())
EOF
cd /tmp/cylab_eps || exit 1
cp -f ./_z_213sc2.bin in213.bin
printf 'academy{LOCAL_TEST_213}\n' > flag.txt
(./213_chall < in213.bin; echo "[exit $?]") 2>&1 | head -6
