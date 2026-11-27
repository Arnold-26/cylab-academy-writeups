#!/bin/bash
cd /tmp/cylab_eps/g383 || exit 1
KEY=58593a7522257f2a95cce9a68886ff78546784ad7db4473dbd91aecd9eefd508
IV=7a12fd4dc1898efcd997a1b9496e7591
for PW in "ccPEcircy0H7CDp9jYim853rzlnUqUiOSV0Y1W2CuibCzX7xFSlzaJdtMinG7M4R2UOhQj" "akalibardzyratrundle" "yone786" "avidreader13"; do
  rm -f t7.bin
  OUT=$(steghide extract -sf 7.bmp -p "$PW" -xf t7.bin -f 2>&1)
  echo "PW=${PW:0:20}... -> $OUT"
  if [ -f t7.bin ]; then
    echo "  taille: $(stat -c%s t7.bin)"
    openssl enc -d -aes-256-cbc -K $KEY -iv $IV -in t7.bin -out t7.txt 2>/dev/null
    echo "  dechiffre: $(head -c 200 t7.txt)"
    grep -aoE "academy\{[^}]*\}|picoCTF\{[^}]*\}" t7.txt t7.bin | head -3
    break
  fi
done
