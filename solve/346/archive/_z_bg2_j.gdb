set pagination off
set confirm off
file /tmp/bg2/_z_bg2
set $map = 0
break *0x8049709
set $cnt = 0
commands
silent
set $cnt = $cnt + 1
set $map = $ebp - 0xa95
printf "hit %d y=%d x=%d tile='%c'(%d)\n", $cnt, *(int*)($ebp-0xaa0), *(int*)($ebp-0xa9c), *(unsigned char*)0x804c040, *(unsigned char*)0x804c040
x/14cb $map+2700
x/24cb $map+2690
if $cnt >= 12
  quit
end
continue
end
run < /tmp/bg2/in1.bin
