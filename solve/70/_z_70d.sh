#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
objdump -d -Mintel 70_investigative-reversing-0-mystery 2>/dev/null | sed -n '/<main>:/,/^$/p' | sed -n '1,140p'
