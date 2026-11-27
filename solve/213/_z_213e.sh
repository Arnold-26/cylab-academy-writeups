#!/bin/bash
cd /mnt/d/ctf-index || exit 1
nasm -f bin -o _z_213sc2.bin _z_213sc2.asm || exit 3
python3 - <<'EOF'
d = open('/mnt/d/ctf-index/_z_213sc2.bin','rb').read()
print("len:", len(d))
print("hex:", d.hex())
EOF
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
cp -f /mnt/d/ctf-index/_z_213sc2.bin in213.bin
printf 'academy{LOCAL_TEST_213}\n' > flag.txt
(./213_chall < in213.bin; echo "[exit $?]") 2>&1 | head -6
