#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
objdump -d -Mintel 458_perplexed 2>/dev/null | sed -n '/<check>:/,/^$/p' | sed -n '40,95p'
