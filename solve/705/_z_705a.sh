#!/bin/bash
D="/mnt/c/Users/arnol/AppData/Local/Temp/cylab_git/705"
cd "$D" || exit 1
OUT=/tmp/repo705
rm -rf "$OUT" && mkdir -p "$OUT"
fls -o 1140736 -r -p disk.img 2>/dev/null | grep -E '\.git/objects' > /tmp/git705.txt || true
wc -l /tmp/git705.txt
awk -F'\t' '/^r\/r/ {print}' /tmp/git705.txt > /tmp/gf705.txt
wc -l /tmp/gf705.txt
while IFS=$'\t' read -r meta path; do
  ino=$(echo "$meta" | sed -E 's/^[^0-9]*([0-9]+).*/\1/')
  [ -z "$ino" ] && continue
  dest="$OUT/${path#*objects/}"
  mkdir -p "$(dirname "$dest")"
  icat -o 1140736 disk.img "$ino" > "$dest" 2>/dev/null
done < /tmp/gf705.txt
echo "fichiers extraits:"
find "$OUT" -type f | wc -l
du -sh "$OUT"
