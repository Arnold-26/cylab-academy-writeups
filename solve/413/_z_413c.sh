#!/bin/bash
cd /tmp || exit 1
SRC=/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/413_disk.flag.img.gz
if [ ! -f t413.img ]; then
  echo "=== decompression ==="
  gunzip -c "$SRC" > t413.img 2>/dev/null || cp "$SRC" t413.img.gz
fi
ls -la t413.img 2>/dev/null
file t413.img 2>/dev/null
echo "=== fichiers interessants (noms) ==="
fls -r -p t413.img 2>/dev/null | grep -aiE "diary|\.txt|history|note|secret|flag|home/" | head -30
echo "=== tailles sous home ==="
fls -r -m / t413.img 2>/dev/null | awk -F'|' '$2 ~ /home\// {printf "%s | size=%s | crtime=%s\n", $2, $7, $11}' | head -25
