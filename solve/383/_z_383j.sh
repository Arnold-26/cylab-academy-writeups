#!/bin/bash
cd /tmp/cylab_eps/g383 || exit 1
for P in chizazerite guldulheen yasuoaatrox yasuoaatrox?; do
  for F in 1.bmp 2.bmp 3.bmp 7.bmp; do
    OUT="try_${P}_${F}.bin"
    rm -f "$OUT"
    steghide extract -sf "$F" -p "$P" -xf "$OUT" -f >/dev/null 2>&1
    if [ -f "$OUT" ]; then
      echo "SUCCES pass=$P fichier=$F -> $(stat -c%s $OUT) octets | $(file -b $OUT | cut -c1-50)"
    fi
  done
done
echo "--- fin ---"
