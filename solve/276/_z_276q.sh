#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
printf 'test123\n' > /tmp/in.txt
gdb -nx -q -batch \
  -ex 'set pagination off' \
  -ex 'set disable-randomization on' \
  -ex 'break *0x555555555442' \
  -ex 'run < /tmp/in.txt' \
  -ex 'x/s $rbp-0x30' \
  -ex 'x/s $rbp-0xb2' \
  --args ./276_keygenme 2>&1 | tail -18
