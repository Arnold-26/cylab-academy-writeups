#!/bin/bash
D="/tmp/cylab_git/707"
cd "$D" || exit 1
echo "=== racine partition 3 ==="
fls -o 1140736 disk.img 2>/dev/null | head -20
echo "=== recherche .git/flag ==="
fls -o 1140736 -r disk.img 2>/dev/null | grep -iE '\.git|flag|home' | head -15
