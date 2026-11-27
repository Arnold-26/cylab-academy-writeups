#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== GOT (relocations) ==="
objdump -R 215_chall 2>/dev/null | grep -E 'printf|atoi|snprintf|puts|read'
echo "=== PLT ==="
objdump -d -j .plt -Mintel 215_chall 2>/dev/null | grep -E '^0+[0-9a-f]+ <|jmp' | head -20
echo "=== main non-PIE ? ==="
readelf -h 215_chall | grep Type
