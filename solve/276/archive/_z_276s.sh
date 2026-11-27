#!/bin/bash
cd /tmp/cylab_eps || exit 1
printf 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n' > /tmp/in36.txt
gdb -nx -q -batch \
  -ex 'set pagination off' \
  -ex 'set disable-randomization on' \
  -ex 'break *0x555555555442' \
  -ex 'run < /tmp/in36.txt' \
  -ex 'x/s $rbp-0x30' \
  -ex 'x/40cb $rbp-0x30' \
  --args ./276_keygenme 2>&1 | tail -18
