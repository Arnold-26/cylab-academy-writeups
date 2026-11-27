#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo 'academy{TESTLOCAL123}' > flag.txt
t() {
  printf '%s\n' "$1" > /tmp/bef.txt
  echo -n "[$1] -> "
  timeout 10 ./217_homework < /tmp/bef.txt 2>&1 | tail -c 150 | tr -d '\0' | tr '\n' '|'
  echo
}
t '88*,@'
t '88*88*+,@'
t '55+,@'
t '8 8*,@'
t '88*:*,@'
t '0!,@'
t '88*0g,@'
