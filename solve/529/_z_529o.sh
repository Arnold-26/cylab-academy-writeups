#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/pb529/dec || exit 1
echo "=== toutes les chaines de MainActivity dans l'ordre ==="
grep -oE 'const-string[^,]*, "[^"]*"' smali_classes3/com/example/picobank/MainActivity.smali | sed 's/.*, //' | nl | head -60
