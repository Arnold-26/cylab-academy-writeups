set pagination off
set confirm off
b exit
run < /tmp/office/in1.txt
printf "=== bss 0x804d050..0x804d080 ===\n"
x/12xw 0x804d050
printf "=== heap maison 0xf7fbd000 (0x3000) ===\n"
x/512xw 0xf7fbd000
