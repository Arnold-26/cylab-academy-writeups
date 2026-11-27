#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
objdump -d -Mintel 146_heapedit 2>/dev/null | sed -n '/<main>:/,/^$/p' | head -80
