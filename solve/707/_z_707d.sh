#!/bin/bash
D="/mnt/c/Users/arnol/AppData/Local/Temp/cylab_git/707"
cd "$D" || exit 1
echo "=== home ==="
fls -o 1140736 disk.img 64770 2>/dev/null | head -10
echo "=== arbo home ==="
fls -o 1140736 -r disk.img 2>/dev/null | sed -n '/home/,+8p' | head -20
