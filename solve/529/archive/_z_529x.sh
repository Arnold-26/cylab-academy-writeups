#!/bin/bash
cd /tmp/cylab_eps/pb529/dec || exit 1
echo "=== tous les montants '\$ ...' de toutes les classes de l'app ==="
grep -rhoE 'const-string[^,]*, "\$ [^"]*"' smali_classes*/com/example/picobank/ 2>/dev/null | sed 's/.*, //' | nl
echo "=== classes de l'app ==="
ls smali_classes*/com/example/picobank/*.smali | sed 's#.*/##'
