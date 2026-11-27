#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== win complete ==="
objdump -d -Mintel --start-address=0x804973f --stop-address=0x804977a 346_game 2>/dev/null | tail -20
echo "=== references au map / gets / fgets dans le jeu ==="
objdump -d -Mintel --start-address=0x8049200 --stop-address=0x8049740 346_game 2>/dev/null | grep -E "call.*(fgets|getchar|scanf|read|puts|printf)|lea +eax,\[ebp|mov +BYTE PTR" | head -30
