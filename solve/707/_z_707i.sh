#!/bin/bash
D="/mnt/c/Users/arnol/AppData/Local/Temp/cylab_git/707"
cd "$D" || exit 1
OUT=/tmp/repo707
rm -rf "$OUT" && mkdir -p "$OUT"
fls -o 1140736 -r -p disk.img 2>/dev/null | grep 'killer-chat-app' > /tmp/list707.txt || true
wc -l /tmp/list707.txt
# extraire les fichiers (pas les repertoires)
awk -F'\t' '/^r\/r/ || /^r\/r \*/ {print}' /tmp/list707.txt > /tmp/files707.txt
wc -l /tmp/files707.txt
while IFS=$'\t' read -r meta path; do
  ino=$(echo "$meta" | sed -E 's/^[^0-9]*([0-9]+).*/\1/')
  [ -z "$ino" ] && continue
  dest="$OUT${path#home/ctf-player/Code/killer-chat-app}"
  mkdir -p "$(dirname "$dest")"
  icat -o 1140736 disk.img "$ino" > "$dest" 2>/dev/null
done < /tmp/files707.txt
echo "=== fichier extraits ==="
find "$OUT" -type f | head -20
echo "=== du ==="
du -sh "$OUT"
