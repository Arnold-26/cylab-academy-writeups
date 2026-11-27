#!/bin/bash
SRC="/mnt/c/Users/arnol/.dsh/attachments/v1/files/85/850cf33d11061c06a3b849bf55f9c9a9e4902cda76dcd4e532f58acc2519389f/timeline-1-partition4.img.gz"
cd /tmp || exit 1
if [ ! -f t721.img ]; then
  echo "=== decompression ==="
  gunzip -c "$SRC" > t721.img
fi
ls -la t721.img
file t721.img
echo "=== timeline (fichiers avec taille) ==="
fls -r -p t721.img 2>/dev/null | head -40
