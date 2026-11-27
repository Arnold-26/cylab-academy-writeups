#!/bin/bash
IMG=~/Downloads/partition4.img
timeout 600 fls -rd -p -m "/" "$IMG" > /tmp/tl721d.txt 2>/dev/null
wc -l /tmp/tl721d.txt
echo "=== entrees supprimees de taille 40-60 octets ==="
awk -F'|' 'NF>=11 && $7+0>=35 && $7+0<=70 {print $7" "$11" "$2}' /tmp/tl721d.txt | sort -k2 -n | tail -20
