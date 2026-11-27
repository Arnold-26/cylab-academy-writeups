#!/bin/bash
B=$(cat ./_z_529base.txt)
cd /tmp/cylab_eps || exit 1
U="$B/download/pico-bank.apk"
echo "URL: $U"
rm -f 529_pico-bank.apk
for i in 1 2 3 4 5 6 7 8; do
  curl -s -m 240 -C - -o 529_pico-bank.apk "$U"
  SZ=$(stat -c%s 529_pico-bank.apk 2>/dev/null || echo 0)
  echo "essai $i -> $SZ octets"
  [ "$SZ" -ge 6600000 ] && break
  sleep 2
done
ls -la 529_pico-bank.apk 2>/dev/null
file 529_pico-bank.apk 2>/dev/null | cut -c1-90
