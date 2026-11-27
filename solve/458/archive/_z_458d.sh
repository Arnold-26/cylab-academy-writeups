#!/bin/bash
cd /tmp/cylab_eps || exit 1
which gdb >/dev/null 2>&1 || { echo "gdb absent"; exit 0; }
cat > /tmp/g458.gdb <<'EOF'
set pagination off
break *0x4011be
run < /dev/null
printf "RBP=%p\n", $rbp
x/32xb $rbp-0x50
x/40cb $rbp-0x50
quit
EOF
gdb -q -batch -x /tmp/g458.gdb ./458_perplexed 2>&1 | tail -20
