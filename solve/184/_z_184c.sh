#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
objdump -d -Mintel 184_fun 2>/dev/null | sed -n '/<main>:/,/^$/p' | sed -n '45,110p'
