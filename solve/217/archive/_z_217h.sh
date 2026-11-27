#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== comparaisons avec 0x67 (g) et 0x70 (p) ==="
objdump -d -Mintel 217_homework 2>/dev/null | grep -nE 'cmp +e?[a-z]+,0x6[70]|cmp +BYTE PTR.*0x6[70]' | head -10
echo "=== contexte autour de la premiere ==="
objdump -d -Mintel 217_homework 2>/dev/null | grep -nE '0x6[70]' | head -10
