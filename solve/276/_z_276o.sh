#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
printf 'test123\n' > /tmp/in.txt
gdb -nx -q -batch \
  -ex 'set pagination off' \
  -ex 'set disable-randomization on' \
  -ex 'starti' \
  -ex 'info proc mappings' \
  --args ./276_keygenme < /tmp/in.txt 2>&1 | grep -E 'keygenme|0x55|0x7f' | head -15
