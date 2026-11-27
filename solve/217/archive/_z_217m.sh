#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo 'academy{TESTLOCAL123}' > flag.txt
t() {
  printf '%s\n' "$1" > /tmp/bef.txt
  echo -n "[$1] -> "
  timeout 10 ./217_homework < /tmp/bef.txt 2>&1 | tail -c 130 | tr -d '\0' | tr '\n' '|'
  echo
}
t '5!@'
t '55!@'
t '5+@'
t '55+@'
t '555++@'
t '555++ !@'
t '9@'
t '99*@'
