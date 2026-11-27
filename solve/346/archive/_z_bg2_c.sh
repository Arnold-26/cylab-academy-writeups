#!/bin/bash
B=./_z_bg2
echo "=== init_player ==="
objdump -d --start-address=0x8049451 --stop-address=0x8049474 -M intel "$B"
echo "=== win ==="
objdump -d --start-address=0x804975d --stop-address=0x80497e0 -M intel "$B"
echo "=== solve_round ==="
objdump -d --start-address=0x8049587 --stop-address=0x8049674 -M intel "$B" | grep -E 'imul|movzbl|mov .*BYTE|cmp|call|ret|jmp|jne|je ' | head -40
echo "=== main (suite) ==="
objdump -d --start-address=0x80496d2 --stop-address=0x804975d -M intel "$B"
