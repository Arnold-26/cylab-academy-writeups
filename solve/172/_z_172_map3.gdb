set pagination off
set confirm off
b exit
run < /tmp/office/in2.txt
set $hb = *(unsigned int*)0x804d064
printf "=== heap base = %p ===\n", $hb
x/72xw $hb
printf "=== bss 0x804d050 ===\n"
x/10xw 0x804d050
