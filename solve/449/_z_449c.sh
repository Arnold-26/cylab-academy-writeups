#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_bin || exit 1
nm -D 449_libc.so.6 2>/dev/null | grep -iE ' (system|setvbuf|puts|printf)@@?' | head -10
echo "---"
readelf -sW 449_libc.so.6 2>/dev/null | grep -iE ' system@| setvbuf@| puts@' | head -6
