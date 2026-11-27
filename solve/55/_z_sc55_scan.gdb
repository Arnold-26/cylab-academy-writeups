set pagination off
set confirm off
file ./_z_55/sice55
break *0x400c14
run
set $base = (unsigned long)((char*)&__malloc_hook - 0x3c4b10)
printf "=== libc base = %#lx ===\n", $base
printf "=== main_arena raw (base+0x3c4b20) ===\n"
x/28gx $base+0x3c4b20
printf "=== _IO_2_1_stdout_ ===\n"
x/30gx (void*)&_IO_2_1_stdout_
printf "=== __free_hook area -0x120 ===\n"
x/40gx (char*)&__free_hook-0x120
printf "=== small qword scan in libc rw (0x3c4000-0x3c8000) ===\n"
set $p = (unsigned long*)($base+0x3c4000)
set $end = (unsigned long*)($base+0x3c8000)
while $p < $end
  set $v = *$p
  if $v >= 0x20 && $v <= 0x67
    printf "OFF %#lx  addr %#lx  val %#lx\n", (unsigned long)$p - $base, (unsigned long)$p, $v
  end
  set $p = $p + 1
end
printf "=== done scan ===\n"
quit
