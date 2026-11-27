#!/bin/bash
cd ./_z_441
nm -D --defined-only 441_libc.so.6 | sort > /tmp/syms.txt
for off in 07782d 07e718 07e96e 0a0f32 0a39b7 0a495d 089ff9; do
  echo "=== offset $off ==="
  awk -v o="0000000000$off" '$1 <= o' /tmp/syms.txt | tail -2
  echo "   -- next --"
  awk -v o="0000000000$off" '$1 > o' /tmp/syms.txt | head -2
done
