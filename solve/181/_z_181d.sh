#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
readelf -h 181_vuln | grep Type
objdump -d -Mintel --start-address=0x8049261 --stop-address=0x80493a0 181_vuln 2>/dev/null | grep -vE "^$" | head -55
