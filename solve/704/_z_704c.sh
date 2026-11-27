#!/bin/bash
D="/mnt/c/Users/arnol/AppData/Local/Temp/cylab_git/704"
cd "$D" || exit 1
IMG=$(ls *.dd | head -1)
icat "$IMG" 532021 > dont-delete.gz 2>/dev/null
ls -la dont-delete.gz
file dont-delete.gz
echo "=== contenu ==="
gunzip -c dont-delete.gz 2>/dev/null | head -10
echo "=== recherche flag ==="
gunzip -c dont-delete.gz 2>/dev/null | grep -aoE 'academy\{[^}]*\}|picoCTF\{[^}]*\}' | head -3
