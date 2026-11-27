#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
wasm2wat 182_wasm.bin -o /tmp/182.wat 2>/dev/null
echo "=== fonctions ==="
grep -n "func " /tmp/182.wat | head -10
echo "=== corps de check_flag ==="
awk '/func \$check_flag/,0' /tmp/182.wat | head -80
