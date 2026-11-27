#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
OFF=731136
for INO in 2386 2365 2366 2408; do
  echo "########## inode $INO ##########"
  icat -o $OFF 383_disk.img $INO 2>/dev/null | head -60
  echo
done
echo "=== galerie / bmp dans l'image ==="
fls -o $OFF -r -p 383_disk.img 2>/dev/null | grep -iE "gallery|\.bmp|\.jpg|\.png" | head -20
