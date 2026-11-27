#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== fonctions restantes ==="
objdump -d -Mintel 346_game 2>/dev/null | grep -E "^[0-9a-f]+ <" | tail -12
echo "=== solve_round / win region (0x8049600-0x8049760) ==="
objdump -d -Mintel --start-address=0x8049600 --stop-address=0x8049760 346_game 2>/dev/null | grep -E "call|cmp|mov +BYTE|lea|jne|je |jmp|push" | head -40
