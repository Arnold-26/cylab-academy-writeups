#!/bin/bash
cd /tmp || exit 1
for OFF in 1140736 2048; do
  echo "=== RACINE partition @ $OFF ==="
  fls -o $OFF -p t413.img 2>/dev/null | head -30
  echo "--- bodyfile racine (noms complets) ---"
  fls -o $OFF -m / t413.img 2>/dev/null | awk -F'|' '{printf "%s | size=%s | inode=%s\n", $2, $7, $3}' | head -20
done
