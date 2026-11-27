#!/bin/bash
cd /tmp/cylab_eps || exit 1
printf 'test123\n' > /tmp/in.txt
gdb -nx -q -batch \
  -ex 'set pagination off' \
  -ex 'set disable-randomization on' \
  -ex 'starti' \
  -ex 'break *0x555555555442' \
  -ex 'continue' \
  -ex 'x/s $rbp-0x30' \
  -ex 'x/s $rbp-0xb2' \
  --args ./276_keygenme < /tmp/in.txt 2>&1 | tail -15
