set pagination off
set confirm off
b exit
run < /tmp/office/in1.txt
printf "=== heap 0x804e000.. ===\n"
x/160xw 0x804e000
printf "=== bss 0x804d000..0x804e000 (variables globales) ===\n"
x/64xw 0x804d000
