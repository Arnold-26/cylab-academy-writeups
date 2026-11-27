#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 54_investigative-reversing-4-mystery
strings -n 4 54_investigative-reversing-4-mystery | grep -aiE "bmp|flag|txt|Item|encoded|original" | head -12
echo "=== boucle principale (constantes) ==="
objdump -d -Mintel 54_investigative-reversing-4-mystery 2>/dev/null | grep -E "mov +DWORD PTR \[rbp-0x[0-9a-f]+\],0x[0-9a-f]+|cmp +DWORD PTR \[rbp-0x[0-9a-f]+\],0x[0-9a-f]+|call.*codedChar" | head -20
