#!/bin/bash
D="/mnt/c/Users/arnol/AppData/Local/Temp/cylab_git/706"
cd "$D" || exit 1
OUT=/tmp/repo706
rm -rf "$OUT" && mkdir -p "$OUT"
fls -o 1140736 -r -p disk.img 2>/dev/null | grep -E '\.git/' > /tmp/git706.txt || true
wc -l /tmp/git706.txt
awk -F'\t' '/^r\/r/ {print}' /tmp/git706.txt > /tmp/gf706.txt
wc -l /tmp/gf706.txt
while IFS=$'\t' read -r meta path; do
  ino=$(echo "$meta" | sed -E 's/^[^0-9]*([0-9]+).*/\1/')
  [ -z "$ino" ] && continue
  dest="$OUT/${path#*/.git/}"
  mkdir -p "$(dirname "$dest")"
  icat -o 1140736 disk.img "$ino" > "$dest" 2>/dev/null
done < /tmp/gf706.txt
echo "fichiers extraits:"; find "$OUT" -type f | wc -l
find "$OUT" -type f | head -20
