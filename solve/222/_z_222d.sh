#!/bin/bash
cd /tmp/cylab_eps || exit 1
cat > /tmp/g222d.gdb <<'EOF'
set pagination off
set confirm off
break *memcmp@plt
run AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
printf "=== RDI ===\n"
x/s $rdi
printf "=== RSI ===\n"
x/s $rsi
printf "RDX: %ld\n", $rdx
printf "=== RDI bytes ===\n"
x/72xb $rdi
printf "=== RSI bytes ===\n"
x/72xb $rsi
quit
EOF
timeout 120 gdb -nx -batch -x /tmp/g222d.gdb ./222_not-crypto 2>&1 | tail -25
