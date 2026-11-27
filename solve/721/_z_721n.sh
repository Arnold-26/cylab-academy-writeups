#!/bin/bash
IMG=/mnt/c/Users/arnol/Downloads/partition4.img
echo "=== recherche base64 de 'academy{' (YWNhZGVte) ==="
timeout 300 grep -aob "YWNhZGVte" "$IMG" | head -10
echo "=== recherche base64 de 'picoCTF{' ==="
timeout 300 grep -aob "cGljb0NUR" "$IMG" | head -10
echo "=== contexte autour de la premiere occurrence ==="
OFF=$(timeout 300 grep -aob "YWNhZGVte" "$IMG" | head -1 | cut -d: -f1)
echo "offset: $OFF"
if [ -n "$OFF" ]; then
  dd if="$IMG" bs=1 skip=$((OFF-200)) count=500 2>/dev/null | strings -n 8 | head -10
fi
