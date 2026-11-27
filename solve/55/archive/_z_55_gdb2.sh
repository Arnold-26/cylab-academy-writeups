#!/bin/bash
cd ./_z_55
cp sice_cream sice55
patchelf --set-interpreter ./_z_55/ld-2.23.so --set-rpath ./_z_55 sice55 2>/dev/null
ldd ./sice55 2>&1 | head -4
cat > dbg55.gdb <<'GDB'
set pagination off
set confirm off
break *0x400ae4
commands
  silent
  printf "=== free(%p)\n", $rdi
  printf "  [rdi-8]=%#lx  [rdi]=%#lx  [rdi+8]=%#lx\n", *(unsigned long*)($rdi-8), *(unsigned long*)$rdi, *(unsigned long*)($rdi+8)
  continue
end
run < in.bin > /dev/null
printf "=== fin\n"
quit
GDB
timeout 120 gdb -q -batch -nx -x dbg55.gdb ./sice55 < /dev/null 2>&1 | head -40
