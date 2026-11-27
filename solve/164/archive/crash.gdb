set pagination off
run < in_exploit.txt
printf "\n=== SIGSEGV ===\n"
printf "rip=%p r13=%p r12=%p rbx=%p\n", $rip, $r13, $r12, $rbx
x/i $rip
printf "valeur pointee par r13 (si lisible) :\n"
x/4gx $r13
printf "--- va_list area ---\n"
x/20gx 0x7fffffffdd70
printf "--- pile au moment du call printf (frame de buy_stonks) ---\n"
frame 3
info registers rbp rsp
x/24gx $rbp-0x40
