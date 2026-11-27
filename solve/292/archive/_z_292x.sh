#!/bin/bash
cd /tmp/cylab_eps || exit 1
python3 ./_z_292w.py
cat > /tmp/g292.gdb <<'EOF'
set pagination off
break *0x0805e4b0
run < in292.bin
printf "INT80 #1 : eax=%d ebx=%p ecx=%p edx=%p\n", $eax, $ebx, $ecx, $edx
continue
printf "INT80 #2 : eax=%d ebx=%p ecx=%p edx=%p\n", $eax, $ebx, $ecx, $edx
x/s $ebx
continue
printf "apres : eip=%p\n", $eip
x/4i $eip
quit
EOF
gdb -nx -q -batch -x /tmp/g292.gdb ./292_vuln 2>&1 | tail -25
