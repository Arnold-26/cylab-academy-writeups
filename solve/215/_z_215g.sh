#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 215_chall
echo "=== main : lea rbp-... ==="
objdump -d -Mintel 215_chall 2>/dev/null | sed -n '/<main>:/,/^$/p' | grep -E 'lea|mov +rsi|call|sub +rsp' | head -30
