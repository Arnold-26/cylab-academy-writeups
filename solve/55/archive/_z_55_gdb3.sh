#!/bin/bash
cd ./_z_55
cat > dbg56.gdb <<'GDB'
set pagination off
set confirm off
break *0x400ae4
commands
  silent
  printf "\n=== free(%p) size_at_p8=%#lx\n", $rdi, *(unsigned long*)($rdi+8)
  continue
end
run < in.bin
printf "=== fin du programme\n"
quit
GDB
timeout 120 gdb -q -batch -nx -x dbg56.gdb ./sice55 < /dev/null 2>&1 | tail -25
