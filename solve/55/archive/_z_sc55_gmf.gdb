set pagination off
set confirm off
file ./_z_55/sice55
break *0x400a38
run < /tmp/sc55/in1.bin
set $base = (unsigned long)((char*)&__malloc_hook - 0x3c4b10)
printf "=== base %#lx ===\n", $base
printf "=== scan qword 0x80 in libc rw ===\n"
set $p = (unsigned long*)($base+0x3c4000)
while $p < (unsigned long*)($base+0x3ca000)
  if *$p == 0x80
    printf "OFF %#lx\n", (unsigned long)$p - $base
  end
  set $p = $p + 1
end
printf "=== scan qword 0x21000 (system_mem) ===\n"
set $p = (unsigned long*)($base+0x3c4000)
while $p < (unsigned long*)($base+0x3ca000)
  if *$p == 0x21000
    printf "OFF %#lx\n", (unsigned long)$p - $base
  end
  set $p = $p + 1
end
printf "=== globals near free_hook ===\n"
x/24gx (char*)&__free_hook-0x40
quit
