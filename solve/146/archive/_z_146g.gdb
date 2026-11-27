set pagination off
break *0x4009c5
run < /dev/null
printf "chunk1=%p\n", *(void**)($rbp-0x98)
printf "chunk7=%p\n", *(void**)($rbp-0x90)
printf "chunk8=%p\n", *(void**)($rbp-0x80)
x/4gx *(void**)($rbp-0x80)
x/8bx *(void**)($rbp-0x98)-0x300
quit
