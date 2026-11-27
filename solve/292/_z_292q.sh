#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
python3 /mnt/d/ctf-index/_z_292p.py
cat > /tmp/g292.gdb <<'EOF'
set pagination off
run < in292.bin
printf "\nEIP=%p\n", $eip
x/6i $eip
info registers eax ebx ecx edx esp ebp
bt
quit
EOF
gdb -nx -q -batch -x /tmp/g292.gdb ./292_vuln 2>&1 | tail -30
