set pagination off
set confirm off
file ./_z_55/sice55
break *0x400c14
run
printf "=== mappings ===\n"
info proc mappings
printf "=== hooks addr ===\n"
p/x (void*)&__malloc_hook
p/x (void*)&__free_hook
p/x (void*)&__realloc_hook
p/x (void*)&__memalign_hook
printf "=== before malloc_hook ===\n"
x/40gx (char*)&__malloc_hook-0x50
printf "=== around free_hook ===\n"
x/40gx (char*)&__free_hook-0x40
printf "=== bss 0x601f80 ===\n"
x/60gx 0x601f80
printf "=== creams/name ===\n"
x/40gx 0x602030
printf "=== main_arena ===\n"
p/x &main_arena
x/8gx &main_arena
quit
