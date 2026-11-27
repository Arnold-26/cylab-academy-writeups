#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
objdump -d -Mintel 27_investigative-reversing-1-mystery 2>/dev/null | sed -n '/<main>:/,/^$/p' | sed -n '120,200p'
