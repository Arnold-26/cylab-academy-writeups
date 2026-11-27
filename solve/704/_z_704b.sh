#!/bin/bash
D="/tmp/cylab_git/704"
cd "$D" || exit 1
IMG=$(ls *.dd | head -1)
echo "=== fichier messages supprime (522629) ==="
icat "$IMG" 522629 2>/dev/null | head -20
echo "=== tous les supprimes ==="
fls -r -d "$IMG" 2>/dev/null | head -10
echo "=== recherche 'flag' dans tous les fichiers ==="
for i in $(fls -r "$IMG" 2>/dev/null | grep -oE '[0-9]+:' | tr -d ':' | head -40); do
  c=$(icat "$IMG" "$i" 2>/dev/null | grep -aoE 'academy\{[^}]*\}|picoCTF\{[^}]*\}' | head -1)
  if [ -n "$c" ]; then echo "inode $i : $c"; fi
done
