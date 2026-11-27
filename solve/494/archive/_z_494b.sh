#!/bin/bash
cd /tmp/cylab_eps/pach/server || exit 1
echo "=== flag.bin ==="
ls -la programs/flag.bin
xxd programs/flag.bin 2>/dev/null | head -10 || python3 -c "d=open('programs/flag.bin','rb').read(); print(d[:200].hex()); print(d[:200])"
echo
echo "=== nand_checker.bin (taille) ==="
ls -la programs/nand_checker.bin
echo
echo "=== index.js : routes ==="
grep -nE "app\.(get|post)|flag|readFile|exec|child" index.js | head -25
echo
echo "=== utils.js ==="
head -40 utils.js
