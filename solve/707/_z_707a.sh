#!/bin/bash
D="/mnt/c/Users/arnol/AppData/Local/Temp/cylab_git/707"
cd "$D" || exit 1
IMG=disk.img
echo "=== fls partition (2048) ==="
fls -o 2048 disk.img 2>/dev/null | head -20
echo "=== recherche .git ==="
fls -o 2048 -r disk.img 2>/dev/null | grep -iE '\.git|flag' | head -15
