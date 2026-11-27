set pagination off
b *0x400ac9
commands
silent
printf "=== avant printf ===\n"
printf "rbp=%p rsp=%p rdi=%p rsi=%p rdx=%p rcx=%p r8=%p r9=%p\n", $rbp, $rsp, $rdi, $rsi, $rdx, $rcx, $r8, $r9
printf "retaddr_slot=%p  value=%p\n", $rbp+8, *(unsigned long*)($rbp+8)
printf "slot[rbp]=%p  value=%p\n", $rbp, *(unsigned long*)$rbp
printf "--- 45 qwords a partir de rsp (arg7 = rsp+8) ---\n"
x/45gx $rsp
continue
end
b *0x400adf
commands
silent
printf "=== avant leave de buy_stonks ===\n"
printf "rdi=%p rsi=%p rax=%p rbp=%p\n", $rdi, $rsi, $rax, $rbp
x/s $rdi
continue
end
run < in_probe.txt
