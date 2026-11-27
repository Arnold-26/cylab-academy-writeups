#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 222_not-crypto
cat > /tmp/g222.gdb <<'EOF'
set pagination off
set confirm off
break memcmp
run AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
printf "RDI: "
x/s $rdi
printf "RSI: "
x/s $rsi
printf "RDX: %ld\n", $rdx
x/80xb $rdi
x/80xb $rsi
quit
EOF
timeout 120 gdb -nx -batch -x /tmp/g222.gdb ./222_not-crypto 2>&1 | tail -30
