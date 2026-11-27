#!/bin/bash
cd /tmp || exit 1
if [ ! -f p3.img ]; then
  echo "=== extraction partition 3 ==="
  dd if=t413.img of=p3.img bs=512 skip=1140736 count=956416 2>/dev/null
fi
ls -la p3.img
echo "=== stat inode 1333 ==="
debugfs -R "stat <1333>" p3.img 2>/dev/null | head -30
echo "=== tentative de lecture du contenu ==="
debugfs -R "cat <1333>" p3.img 2>/dev/null | head -c 1000
echo
echo "=== stat inode 1844 (innocuous-file.txt) ==="
debugfs -R "cat <1844>" p3.img 2>/dev/null | head -c 300
