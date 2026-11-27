#!/bin/bash
cd /tmp || exit 1
echo "=== recherche directe du flag dans l image ==="
grep -aoE "academy\{[^}]{2,80}\}" t413.img 2>/dev/null | head -5
echo "=== recherche de 'picoCTF{' aussi ==="
grep -aoE "picoCTF\{[^}]{2,80}\}" t413.img 2>/dev/null | head -3
echo "=== entrees supprimees sous home (partition 3) ==="
fls -o 1140736 -r -d -p t413.img 2>/dev/null | head -25
