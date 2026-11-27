#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
cp /mnt/d/ctf-index/_z_hook2.c hook2.c
gcc -shared -fPIC -o hook2.so hook2.c -ldl 2>&1 | head -5
echo "=== run avec hook2 ==="
echo "test123" | LD_PRELOAD=./hook2.so ./276_keygenme 2>&1 | head -25
