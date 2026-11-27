#!/bin/bash
cd /tmp/cylab_eps || exit 1
cat > /tmp/g222b.gdb <<'EOF'
set pagination off
set confirm off
break memcmp if $rdx > 16
run AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
printf "RDI: "
x/s $rdi
printf "RSI: "
x/s $rsi
printf "RDX: %ld\n", $rdx
x/72xb $rdi
x/72xb $rsi
quit
EOF
timeout 120 gdb -nx -batch -x /tmp/g222b.gdb ./222_not-crypto 2>&1 | tail -20
