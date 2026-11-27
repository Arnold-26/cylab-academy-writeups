set pagination off
set confirm off
file /mnt/d/ctf-index/_z_55/sice55
break *0x400a38
run < /tmp/sc55/in1.bin
set $base = (unsigned long)((char*)&__malloc_hook - 0x3c4b10)
printf "=== libc base %#lx ===\n", $base
printf "=== arena @ %#lx ===\n", $base+0x3c4b20
x/60gx $base+0x3c4b20
printf "=== creams ===\n"
x/8gx 0x602140
quit
