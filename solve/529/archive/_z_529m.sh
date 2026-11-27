#!/bin/bash
cd /tmp/cylab_eps/pb529/dec || exit 1
for F in smali_classes3/com/example/picobank/OTP\$1.smali smali_classes3/com/example/picobank/Notification\$1.smali smali_classes3/com/example/picobank/MainActivity\$1.smali; do
  [ -f "$F" ] || continue
  echo "########## $F ##########"
  grep -oE 'const-string[^,]*, "[^"]*"' "$F" | head -20
  echo "--- comparaisons / logique ---"
  grep -nE "equals|const-string|if-eqz|if-nez|invoke-static|Intent" "$F" | head -25
  echo
done
