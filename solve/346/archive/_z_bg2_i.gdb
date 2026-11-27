set pagination off
set confirm off
file /tmp/bg2/_z_bg2
break *0x8049709
set $cnt = 0
commands
silent
set $cnt = $cnt + 1
printf "=== hit %d  ebp=%p  savedecx=%p  savedebx=%p  savedebp=%p\n", $cnt, $ebp, *(int*)($ebp-8), *(int*)($ebp-4), *(int*)($ebp)
printf "player y=%d x=%d tile=%d\n", *(int*)($ebp-0xaa0), *(int*)($ebp-0xa9c), *(unsigned char*)0x804c040
printf "map[0..8]  : "
x/9bx $ebp-0xa95
printf "near end (ebp-0x20 .. ebp+0x10):\n"
x/48bx $ebp-0x20
if $cnt >= 8
  quit
end
continue
end
run < /tmp/bg2/in1.bin
