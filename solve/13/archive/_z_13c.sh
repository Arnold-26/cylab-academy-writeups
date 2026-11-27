#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== _start ==="
objdump -d -Mintel 13_investigative-reversing-2-mystery 2>/dev/null | sed -n '/<_start>:/,/^$/p' | head -12
echo "=== main : boucle principale ==="
MAIN=$(objdump -d -Mintel 13_investigative-reversing-2-mystery 2>/dev/null | sed -n '/<_start>:/,/^$/p' | grep -oE "0x[0-9a-f]+" | tail -3 | head -1)
objdump -d -Mintel 13_investigative-reversing-2-mystery 2>/dev/null | sed -n '/<main>:/,/^$/p' | grep -E "codedChar|call|movzx|cmp|add|shl|imul|lea" | head -40
