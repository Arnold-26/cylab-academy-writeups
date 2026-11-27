set pagination off
set confirm off
break *0x808ba5c
commands
  silent
  printf "== VULN REACHED ==\n"
  continue
end
break *0x8049261
commands
  silent
  printf "%u\n", *(unsigned int*)($esp+4)
  continue
end
run < /tmp/bizz_in.bin
printf "== END ==\n"
quit
