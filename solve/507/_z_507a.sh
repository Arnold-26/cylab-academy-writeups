#!/bin/bash
D="/mnt/c/Users/arnol/AppData/Local/Temp/cylab_git/507"
cd "$D" || exit 1
IMG=$(ls *.dd | head -1)
icat "$IMG" 522628 > flag.gz 2>/dev/null
ls -la flag.gz
file flag.gz
echo "=== contenu ==="
gunzip -c flag.gz 2>/dev/null | head -5
echo
echo "=== recherche dans le chemin complet ==="
fls -r "$IMG" 2>/dev/null | grep -B2 -A2 'flag.gz' | head -10
