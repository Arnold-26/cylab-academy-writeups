#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
rm -rf y483 && mkdir -p y483 && cd y483 || exit 1
unzip -o -P picoctf ../483_suspicious.zip >/dev/null 2>&1
ls -la
echo "=== file ==="
for f in *; do [ -f "$f" ] && file "$f" | cut -c1-130; done
echo "=== strings interessantes ==="
for f in *; do
  [ -f "$f" ] || continue
  strings -n 6 "$f" 2>/dev/null | grep -aiE "academy|picoCTF|flag|powershell|http|cmd|CreateFile|WriteFile" | head -15
done
echo "=== recherche directe de flag ==="
for f in *; do [ -f "$f" ] && strings "$f" 2>/dev/null | grep -aoE "(academy|picoCTF)\{[^}]{0,80}\}"; done
