#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x149b --stop-address=0x1600 276_keygenme 2>/dev/null | tail -55
