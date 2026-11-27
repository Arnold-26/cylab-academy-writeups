#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== fonction 0x4009c2 ==="
objdump -d -Mintel --start-address=0x4009c2 --stop-address=0x400b40 75_zero_to_hero 2>/dev/null | grep -vE "^$" | head -45
echo "=== main 0x400c62 ==="
objdump -d -Mintel --start-address=0x400c62 --stop-address=0x400de0 75_zero_to_hero 2>/dev/null | grep -vE "^$" | head -50
