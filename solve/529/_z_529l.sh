#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/pb529/dec || exit 1
F=smali_classes3/com/example/picobank/Login\$1.smali
echo "=== chaines ==="
grep -oE 'const-string[^,]*, "[^"]*"' "$F" | head -40
echo "=== corps ==="
wc -l "$F"
sed -n '1,160p' "$F"
