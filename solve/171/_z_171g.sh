#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x80eade0 --stop-address=0x80eaf80 171_enter_password 2>/dev/null | head -60
echo "=== get_flag ==="
objdump -d -Mintel --start-address=0x80eacc0 --stop-address=0x80eade0 171_enter_password 2>/dev/null | grep -E "call|lea|mov +DWORD PTR \[esp" | head -20
