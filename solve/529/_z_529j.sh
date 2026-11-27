#!/bin/bash
cd /tmp/cylab_eps || exit 1
rm -rf pb529 && mkdir -p pb529 && cd pb529 || exit 1
apktool d -f -q ../529_pico-bank.apk -o dec >/dev/null 2>&1
echo "=== recherche de flag en clair dans le decode ==="
grep -rail "academy{" dec 2>/dev/null | head -5
echo "=== classes propres a l'app ==="
find dec -name "*.smali" -path "*picobank*" 2>/dev/null | head -20
find dec -name "*.smali" | grep -viE "androidx|kotlin|com/google" | head -25
echo "=== strings.xml (extrait interessant) ==="
grep -iE "banana|pico|pass|user|flag|secret|key" dec/res/values/strings.xml 2>/dev/null | head -20
