#!/bin/bash
cd /tmp/cylab_eps/pb529/dec || exit 1
echo "=== URLs dans les classes de l'app ==="
grep -rhoE 'const-string[^,]*, "https?://[^"]*"' smali_classes3/com/example/picobank/ 2>/dev/null | sort -u
echo "=== toutes les chaines des classes de l'app ==="
for F in smali_classes3/com/example/picobank/*.smali; do
  echo "--- $(basename $F) ---"
  grep -oE 'const-string[^,]*, "[^"]{3,}"' "$F" | sed 's/.*, //' | head -15
done
echo "=== OTP access\$400 ==="
sed -n '/method.*access\$400/,/end method/p' smali_classes3/com/example/picobank/OTP.smali | head -40
