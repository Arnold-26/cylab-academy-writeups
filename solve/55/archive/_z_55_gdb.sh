#!/bin/bash
cd ./_z_55
cp ../_z_55_gen.py .
python3 _z_55_gen.py
cat > /tmp/dbg55.gdb <<'GDB'
set pagination off
set confirm off
break *0x400ae4
commands
  silent
  printf "=== free(%p)\n", $rdi
  printf "  [rdi-8]=%#lx  [rdi]=%#lx\n", *(unsigned long*)($rdi-8), *(unsigned long*)$rdi
  printf "  main_arena.top = %p\n", *(void**)0x3c4b20+0x60
  continue
end
run < in.bin
printf "=== fin (code %d)\n", $_siginfo
quit
GDB
cp /tmp/dbg55.gdb dbg55.gdb
timeout 120 gdb -q -batch -nx -x dbg55.gdb --args ./ld-2.23.so --library-path ./_z_55 ./sice_cream < /dev/null 2>&1 | head -40
