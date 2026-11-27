#!/bin/bash
D="/tmp/cylab_git/707"
cd "$D" || exit 1
rm -rf recovered && mkdir recovered
timeout 600 tsk_recover -o 1140736 disk.img recovered 2>&1 | tail -2
echo "=== contenu ==="
find recovered -maxdepth 4 -type d -name '.git' 2>/dev/null | head -3
find recovered -maxdepth 5 -type f 2>/dev/null | head -15
