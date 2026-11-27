#!/bin/bash
B=/tmp/bg2/_z_bg2
echo "=== nm T/t ==="
nm "$B" | grep -E ' [Tt] ' | sort
echo
echo "=== full disasm main+move+win+solve ==="
objdump -d -M intel "$B" | sed -n '/<main>:/,/^$/p'
echo "=== move_player ==="
objdump -d -M intel "$B" | sed -n '/<move_player>:/,/^$/p'
echo "=== solve_round ==="
objdump -d -M intel "$B" | sed -n '/<solve_round>:/,/^$/p'
echo "=== init_player ==="
objdump -d -M intel "$B" | sed -n '/<init_player>:/,/^$/p'
echo "=== win ==="
objdump -d -M intel "$B" | sed -n '/<win>:/,/^$/p'
echo "=== __libc_csu / _start refs to main ==="
objdump -d -M intel "$B" | sed -n '/<_start>:/,/^$/p' | head -40
