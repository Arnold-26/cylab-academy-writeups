#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== fonctions du PE (objdump) ==="
objdump -d 57_win-exec-1.exe 2>/dev/null | grep -E "^[0-9a-f]+ <" | grep -viE "plt|dll|_init|_fini" | head -20
echo "=== recherche de la reference au prefixe flag ==="
objdump -d 57_win-exec-1.exe 2>/dev/null | grep -B2 -A6 "academy" | head -20
