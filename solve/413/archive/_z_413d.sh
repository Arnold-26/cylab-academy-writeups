#!/bin/bash
cd /tmp || exit 1
for OFF in 1140736 2048 616448; do
  echo "=== partition @ secteur $OFF ==="
  fls -o $OFF -r -p t413.img 2>/dev/null | head -25
  echo "--- fichiers sous home (taille/crtime) ---"
  fls -o $OFF -r -m / t413.img 2>/dev/null | awk -F'|' '$2 ~ /home/ {printf "%s | size=%s | cr=%s\n", $2, $7, $11}' | head -20
done
