set pagination off
set confirm off
break *0x810aab4
commands
  silent
  printf "=== ENTered 0x810aab4 (parent ladder stage) ===\n"
  continue
end
break *0x808ba1f
commands
  silent
  printf "=== ENTered 0x808ba1f (has_bof) ===\n"
  continue
end
break *0x808ba5c
commands
  silent
  printf "=== VULN fgets 0x15c REACHED ===\n"
  bt 6
  continue
end
break *0x8049261
commands
  silent
  printf "play target=%u\n", *(unsigned int*)($esp+4)
  continue
end
run < in.txt
printf "=== program ended ===\n"
quit
