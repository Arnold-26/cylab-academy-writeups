#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
F=529_pico-bank.apk
U="http://chatelaine.cylabacademy.net:48796/download/pico-bank.apk"
for i in 1 2 3 4 5 6; do
  curl -s -m 300 -C - -o "$F" "$U" 2>/dev/null
  SZ=$(stat -c%s "$F" 2>/dev/null || echo 0)
  echo "essai $i -> $SZ octets"
  if [ "$SZ" -ge 6676557 ]; then break; fi
  sleep 2
done
ls -la "$F"
file "$F" | cut -c1-100
