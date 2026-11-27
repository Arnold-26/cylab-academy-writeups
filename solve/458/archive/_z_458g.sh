#!/bin/bash
cd /tmp/cylab_eps || exit 1
python3 -c "open('/tmp/in458.txt','w').write('A'*26+'\n')"
cat > /tmp/g458.gdb <<'EOF'
set pagination off
break *0x4011be
run < /tmp/in458.txt
printf "RBP=%p\n", $rbp
x/27xb $rbp-0x50
x/27cb $rbp-0x50
quit
EOF
gdb -nx -q -batch -x /tmp/g458.gdb ./458_perplexed 2>&1 | tail -12
