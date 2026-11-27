b *0x804953f
run < _z_bg2_in.txt
printf "eax (write addr) = %p\n", $eax
printf "move_player ebp  = %p\n", $ebp
printf "main ebp         = %p\n", *(unsigned int*)$ebp
printf "ret slot         = %p\n", (char*)(*(unsigned int*)$ebp) - 0xabc
printf "map base         = %p\n", (char*)(*(unsigned int*)$ebp) - 0xa95
printf "ret value        = %p\n", *(unsigned int*)((*(unsigned int*)$ebp) - 0xabc)
printf "offset from map  = %d\n", (int)((char*)((*(unsigned int*)$ebp) - 0xabc) - ((char*)(*(unsigned int*)$ebp) - 0xa95))
x/4wx (*(unsigned int*)$ebp) - 0xac0
