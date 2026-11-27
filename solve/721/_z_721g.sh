#!/bin/bash
echo "=== 5 premieres lignes ==="
head -5 /tmp/tl721.txt
echo "=== champs d'une ligne ==="
head -1 /tmp/tl721.txt | awk -F'|' '{for(i=1;i<=NF;i++) print i": "$i}'
echo "=== 20 dernieres lignes brutes ==="
grep -v "^0|" /tmp/tl721.txt | tail -20
