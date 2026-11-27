#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== PLT ==="
objdump -d -j .plt -Mintel 222_not-crypto 2>/dev/null | head -25
echo "=== relocations ==="
objdump -R 222_not-crypto 2>/dev/null | grep -i memcmp
echo "=== appels vers memcmp ==="
objdump -d -Mintel 222_not-crypto 2>/dev/null | grep -n 'memcmp' | head -5
