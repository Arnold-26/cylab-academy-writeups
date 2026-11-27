#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== codedChar ==="
objdump -d -Mintel 13_investigative-reversing-2-mystery 2>/dev/null | sed -n '/<codedChar>:/,/^$/p' | head -40
echo "=== main (recherche) ==="
objdump -d -Mintel 13_investigative-reversing-2-mystery 2>/dev/null | grep -E "^0[0-9a-f]+ <" | head -12
