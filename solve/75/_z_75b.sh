#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x4008b0 --stop-address=0x400b40 75_zero_to_hero 2>/dev/null | head -90
