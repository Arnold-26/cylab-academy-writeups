#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== symboles ==="
nm 70_investigative-reversing-0-mystery 2>/dev/null | grep -E " T | t " | head -15
echo "=== fonctions : insert / main ==="
objdump -d -Mintel 70_investigative-reversing-0-mystery 2>/dev/null | grep -E "^0[0-9a-f]+ <" | head -15
echo "=== corps de insert (si present) ==="
objdump -d -Mintel 70_investigative-reversing-0-mystery 2>/dev/null | sed -n '/<insert>:/,/^$/p' | head -50
