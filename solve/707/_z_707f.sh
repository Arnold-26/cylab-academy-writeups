#!/bin/bash
D="/mnt/c/Users/arnol/AppData/Local/Temp/cylab_git/707"
cd "$D" || exit 1
echo "=== .git (inode 65662) ==="
fls -o 1140736 disk.img 65662 2>/dev/null | head -25
echo "=== refs/logs ==="
fls -o 1140736 -r disk.img 2>/dev/null | grep -E 'refs|logs|HEAD|COMMIT|pack' | head -20
