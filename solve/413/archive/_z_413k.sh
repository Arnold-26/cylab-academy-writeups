#!/bin/bash
cd /tmp || exit 1
echo "=== noms sur une zone large (600032000..600050000) ==="
dd if=t413.img bs=1 skip=600032000 count=18000 2>/dev/null | strings -n 5 | head -60
echo "=== recherche d un nom contenant academy/flag/secret ==="
dd if=t413.img bs=1 skip=600032000 count=18000 2>/dev/null | strings -n 4 | grep -aiE "academy|flag|secret|diary|final" | head -10
