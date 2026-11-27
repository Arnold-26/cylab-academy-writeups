#!/bin/bash
D="/mnt/c/Users/arnol/AppData/Local/Temp/cylab_git/706"
cd "$D" || exit 1
gunzip -kf disk.img.gz 2>&1 | tail -1
ls -la disk.img 2>/dev/null
mmls disk.img 2>/dev/null | head -8
echo "=== recherche .git ==="
fls -o 1140736 -r disk.img 2>/dev/null | grep -E '\.git|flag' | head -10
