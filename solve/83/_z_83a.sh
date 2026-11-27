#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 83_investigative-reversing-3-mystery 2>/dev/null
file 83_investigative-reversing-3-mystery | cut -c1-100
echo "=== chaines ==="
strings -n 5 83_investigative-reversing-3-mystery | grep -aiE "flag|bmp|png|original|encoded|not found|missing" | head -10
echo "=== symboles ==="
objdump -d -Mintel 83_investigative-reversing-3-mystery 2>/dev/null | grep -E "^[0-9a-f]+ <" | head -12
echo "=== boucle encodage (autour des fputc) ==="
objdump -d -Mintel 83_investigative-reversing-3-mystery 2>/dev/null | grep -B10 "call.*fputc" | head -40
