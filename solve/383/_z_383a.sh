#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
if [ ! -f 383_disk.img ]; then
  echo "decompression..."
  gunzip -c 383_disk.flag.img.gz > 383_disk.img
fi
ls -la 383_disk.img
file 383_disk.img
echo "=== table de partitions ==="
mmls 383_disk.img 2>/dev/null | head -15
echo "=== recherche directe du flag ==="
grep -aoE "(academy|picoCTF)\{[^}]{4,80}\}" 383_disk.img | head -5
echo "=== systeme de fichiers ==="
fsstat 383_disk.img 2>/dev/null | head -12
