#!/bin/bash
cd /tmp/cylab_eps/g383 || exit 1
KEY=58593a7522257f2a95cce9a68886ff78546784ad7db4473dbd91aecd9eefd508
IV=7a12fd4dc1898efcd997a1b9496e7591
for F in out_1.bmp.bin out_2.bmp.bin out_3.bmp.bin; do
  echo "=== $F ==="
  echo -n "  entete: "; head -c 16 "$F" | xxd | head -1
  openssl enc -d -aes-256-cbc -K $KEY -iv $IV -in "$F" -out "dec_$F" 2>&1 | tail -2
  if [ -f "dec_$F" ]; then
    echo -n "  dechiffre: $(stat -c%s dec_$F) octets | type: "; file -b "dec_$F"
    echo -n "  debut: "; head -c 80 "dec_$F" | strings | head -2
    grep -aoE "(academy|picoCTF)\{[^}]{4,80}\}" "dec_$F" | head -2
  fi
done
