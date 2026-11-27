#!/bin/bash
cd /tmp/cylab_eps/pb529/dec || exit 1
echo "########## OTP\$2.smali ##########"
cat smali_classes3/com/example/picobank/OTP\$2.smali 2>/dev/null | head -120
