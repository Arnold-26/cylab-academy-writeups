#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== solve_round 346 (debut) ==="
objdump -d -Mintel --start-address=0x8049587 --stop-address=0x8049640 346_game 2>/dev/null | head -30
echo "=== init_map 346 : dimensions ==="
objdump -d -Mintel --start-address=0x8049223 --stop-address=0x80492c9 346_game 2>/dev/null | grep -E "cmp|imul|mov BYTE|0x1d|0x59" | head -10
