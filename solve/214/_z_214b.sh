#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== setup ==="
objdump -d -Mintel --start-address=0x4008a7 --stop-address=0x400a00 214_horse 2>/dev/null | grep -E "mov|call|lea|push" | head -30
echo "=== main ==="
objdump -d -Mintel --start-address=0x400a00 --stop-address=0x400b80 214_horse 2>/dev/null | grep -E "mov|call|lea|cmp|j" | head -40
