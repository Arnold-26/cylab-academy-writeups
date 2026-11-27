#!/bin/bash
cd /tmp/cylab_eps/pb529/dec || exit 1
echo "=== URLs http dans tout le decode (hors libs) ==="
grep -rhoE 'const-string[^,]*, "https?://[^"]*"' smali_classes3/ smali_classes2/ 2>/dev/null | sed 's/.*, //' | sort -u | head -20
echo "=== 'your server url' contexte ==="
grep -rn -B4 -A6 "your server url" smali_classes3/com/example/picobank/OTP.smali 2>/dev/null | head -30
echo "=== verify-otp contexte ==="
grep -rn -B6 -A10 '"/verify-otp"' smali_classes3/ 2>/dev/null | head -40
