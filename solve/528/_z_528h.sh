#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
which apktool >/dev/null 2>&1 || { echo "apktool absent"; echo arnold | sudo -S apt-get install -y -qq apktool 2>&1 | tail -2; }
rm -rf m528 && mkdir -p m528 && cd m528 || exit 1
apktool d -f -q ../528_minions.apk >/dev/null 2>&1
echo "=== arborescence (hors smali) ==="
find . -type f ! -path "./smali*" | head -40
echo "=== recherche flag dans tout le decode ==="
grep -rail "academy{" . 2>/dev/null | head -10
grep -rail "picoctf{" . 2>/dev/null | head -10
echo "=== strings.xml ==="
cat res/values/strings.xml 2>/dev/null | head -40
