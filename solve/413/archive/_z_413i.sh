#!/bin/bash
cd /tmp || exit 1
echo "=== dump autour de 600033312 ==="
dd if=t413.img bs=1 skip=600033200 count=500 2>/dev/null | od -c | head -40
echo "=== recherche de noms lisibles dans la zone ==="
dd if=t413.img bs=1 skip=600033000 count=4000 2>/dev/null | strings -n 4 | head -40
