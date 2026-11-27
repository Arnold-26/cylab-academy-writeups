#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
rm -rf b56 && mkdir -p b56 && cd b56 || exit 1
unzip -o ../56_b1g_mac.zip >/dev/null 2>&1
ls -la
echo "=== file ==="
file main.exe | cut -c1-140
echo "=== strings interessantes ==="
strings -n 6 main.exe | grep -aiE "academy|picoCTF|flag|secret" | head -20
echo "=== recherche d'un flag direct ==="
strings main.exe | grep -aoE "(academy|picoCTF)\{[^}]{0,80}\}" | head -5
