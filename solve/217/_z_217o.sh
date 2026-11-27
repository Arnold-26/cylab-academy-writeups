#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== 0x1d8a (handler par defaut) ==="
objdump -d -Mintel --start-address=0x1d8a --stop-address=0x1e20 217_homework 2>/dev/null | tail -35
