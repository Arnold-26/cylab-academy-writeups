#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== taille de check ==="
objdump -d -Mintel 458_perplexed 2>/dev/null | sed -n '/<check>:/,/^$/p' | wc -l
echo "=== check (extrait) ==="
objdump -d -Mintel 458_perplexed 2>/dev/null | sed -n '/<check>:/,/^$/p' | head -60
echo "..."
echo "=== references aux donnees (.rodata) ==="
objdump -d -Mintel 458_perplexed 2>/dev/null | sed -n '/<check>:/,/^$/p' | grep -oE "# 40[0-9a-f]+" | sort -u | head -20
