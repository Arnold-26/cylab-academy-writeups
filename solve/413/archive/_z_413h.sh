#!/bin/bash
cd /tmp || exit 1
echo "=== noms recherches dans les donnees brutes ==="
for n in "its-all-in-the-name" "innocuous-file" "force-wait"; do
  echo "--- $n ---"
  grep -ac "$n" t413.img 2>/dev/null
  grep -aob "$n" t413.img 2>/dev/null | head -3
done
echo "=== entrees supprimees a la racine de la partition 3 ==="
fls -o 1140736 -d -p t413.img 2>/dev/null | head -20
