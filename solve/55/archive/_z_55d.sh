#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x400b56 --stop-address=0x400c20 55_sice_cream 2>/dev/null | grep -vE "^$"
echo "=== fonction eat (0x4009f0-0x400a70) ==="
objdump -d -Mintel --start-address=0x4009f0 --stop-address=0x400a70 55_sice_cream 2>/dev/null | grep -vE "^$" | head -30
