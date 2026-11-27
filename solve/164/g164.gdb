set pagination off
set confirm off
break *0x400ac9
commands
  silent
  printf "=== printf(user_buf=%p)  rbp=%p rsp=%p\n", $rdi, $rbp, $rsp
  printf "buy_stonks ret addr slot = %p (valeur %p)\n", $rbp+8, *(void**)($rbp+8)
  printf "arg_slots (rsp): \n"
  x/24gx $rsp
  printf "--- au dessus de rbp:\n"
  x/16gx $rbp
  continue
end
run
