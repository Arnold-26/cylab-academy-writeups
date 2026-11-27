#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== recherche du handler de chiffres (sub ...,0x30) ==="
objdump -d -Mintel 217_homework 2>/dev/null | grep -nE 'sub +e?[a-z]+,0x30|cmp +e?[a-z]+,0x9|lea +e?[a-z]+,\[.*-0x30\]' | head -10
echo "=== debut de step ==="
objdump -d -Mintel 217_homework 2>/dev/null | sed -n '/<step>:/,/^$/p' | head -45
