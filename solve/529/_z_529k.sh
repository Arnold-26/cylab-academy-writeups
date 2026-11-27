#!/bin/bash
cd /tmp/cylab_eps/pb529/dec || exit 1
F=smali_classes3/com/example/picobank/Login.smali
echo "=== taille ==="
wc -l "$F"
echo "=== chaines de Login.smali ==="
grep -oE 'const-string[^,]*, "[^"]*"' "$F" | head -40
echo "=== corps (extrait) ==="
sed -n '1,120p' "$F"
