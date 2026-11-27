#!/bin/bash
D="/mnt/c/Users/arnol/AppData/Local/Temp/cylab_git/704"
cd "$D" || exit 1
IMG=$(ls *.dd | head -1)
echo "=== log dir ==="
fls "$IMG" 4 2>/dev/null | head -15
echo "=== recursif ==="
fls -r "$IMG" 2>/dev/null | head -25
echo "=== recherche flag ==="
grep -aoE 'academy\{[^}]*\}|picoCTF\{[^}]*\}' "$IMG" 2>/dev/null | sort -u | head -5
