#!/bin/bash
cd /tmp/cylab_eps || exit 1
cat > /tmp/g458.gdb <<'EOF'
set pagination off
break *0x4011be
run < /dev/null
printf "RBP=%p\n", $rbp
x/27xb $rbp-0x50
x/28cb $rbp-0x50
quit
EOF
gdb -nx -q -batch -x /tmp/g458.gdb ./458_perplexed 2>&1 | tail -12
