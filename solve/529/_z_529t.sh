#!/bin/bash
cd /tmp/cylab_eps/pb529/dec || exit 1
echo "=== constructeur Transaction ==="
grep -A8 "method public constructor <init>" smali_classes3/com/example/picobank/Transaction.smali | head -20
echo "=== un appel new-instance Transaction dans MainActivity (contexte) ==="
grep -n -A18 "new-instance .*Lcom/example/picobank/Transaction;" smali_classes3/com/example/picobank/MainActivity.smali | head -50
