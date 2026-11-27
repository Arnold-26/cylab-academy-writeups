#!/bin/bash
IMG=/mnt/c/Users/arnol/Downloads/partition4.img
timeout 600 fls -r -p -m "/" "$IMG" > /tmp/tl721.txt 2>/dev/null
echo "lignes: $(wc -l < /tmp/tl721.txt)"
echo "=== 25 entrees les plus recentes ==="
grep -v "^0|" /tmp/tl721.txt | awk -F'|' 'NF>=10 {print $3"|"$4"|"$5"|"$9"|"$10"|"$11}' | sort -t'|' -k3 | tail -25
