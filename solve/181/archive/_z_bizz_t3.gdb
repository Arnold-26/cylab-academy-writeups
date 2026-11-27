set pagination off
set confirm off
break *0x808ba5c
commands
  silent
  printf "VULNREACHED\n"
  continue
end
break *0x8049261
commands
  silent
  printf "PLAY %u\n", *(unsigned int*)($esp+4)
  continue
end
run < /tmp/bizz_in.bin > /dev/null
printf "END\n"
quit
