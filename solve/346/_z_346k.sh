#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== boucle principale (0x8049460-0x8049560) ==="
objdump -d -Mintel --start-address=0x8049460 --stop-address=0x8049560 346_game 2>/dev/null | tail -50
