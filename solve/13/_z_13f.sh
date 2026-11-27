#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
objdump -d -Mintel 13_investigative-reversing-2-mystery 2>/dev/null | sed -n '/<main>:/,/^$/p' | sed -n '1,120p'
