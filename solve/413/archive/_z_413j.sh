#!/bin/bash
cd /tmp || exit 1
OFF=1140736
echo "=== innocuous-file.txt (inode 1844) ==="
icat -o $OFF t413.img 1844 2>/dev/null | od -c | head -6
echo "=== its-all-in-the-name (inode 1333) ==="
icat -o $OFF t413.img 1333 2>/dev/null | head -c 1200
echo
echo "=== recherche de flag dans les deux ==="
icat -o $OFF t413.img 1333 2>/dev/null | grep -aoE "academy\{[^}]*\}|picoCTF\{[^}]*\}" | head -3
icat -o $OFF t413.img 1844 2>/dev/null | grep -aoE "academy\{[^}]*\}|picoCTF\{[^}]*\}" | head -3
