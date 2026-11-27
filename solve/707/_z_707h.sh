#!/bin/bash
D="/mnt/c/Users/arnol/AppData/Local/Temp/cylab_git/707"
cd "$D" || exit 1
OUT=/tmp/repo707
rm -rf "$OUT" && mkdir -p "$OUT"
# lister les chemins avec inodes
fls -o 1140736 -r -p disk.img 2>/dev/null | grep 'killer-chat-app' | head -80 > /tmp/list707.txt
wc -l /tmp/list707.txt
head -5 /tmp/list707.txt
# extraire chaque fichier
while IFS= read -r line; do
  ino=$(echo "$line" | grep -oE '^[a-z]+/[a-z]+ [0-9]+' | awk '{print $2}')
  path=$(echo "$line" | grep -oE '/home/.*' | head -1)
  [ -z "$ino" ] && continue
  [ -z "$path" ] && continue
  dest="$OUT${path#/home/ctf-player/Code/killer-chat-app}"
  mkdir -p "$(dirname "$dest")"
  icat -o 1140736 disk.img "$ino" > "$dest" 2>/dev/null
done < /tmp/list707.txt
echo "=== extrait ==="
find "$OUT" -type f | head -15
echo "=== taille ==="
du -sh "$OUT"
