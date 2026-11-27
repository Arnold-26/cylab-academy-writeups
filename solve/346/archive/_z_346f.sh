#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== fonctions ==="
objdump -d -Mintel 346_game 2>/dev/null | grep -E "^[0-9a-f]+ <" | head -20
echo "=== references a You win / flag.txt ==="
objdump -d -Mintel 346_game 2>/dev/null | grep -B6 -A10 "You win" | head -30
echo "=== autour de fopen ==="
objdump -d -Mintel 346_game 2>/dev/null | grep -B10 "call.*fopen" | head -25
