#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
objdump -d 219_riscy 2>/dev/null | sed -n '/10186:/,/10210:/p'
