#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
objdump -d -Mintel --start-address=0x17aa --stop-address=0x18c0 151_remote 2>/dev/null | head -70
