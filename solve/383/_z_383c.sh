#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/g383 || exit 1
KEY=58593a7522257f2a95cce9a68886ff78546784ad7db4473dbd91aecd9eefd508
IV=7a12fd4dc1898efcd997a1b9496e7591
for i in 1 2 3 7; do
  echo "=== steghide $i.bmp ==="
  rm -f "s$i.bin"
  steghide extract -sf "$i.bmp" -p "akalibardzyratrundle" -xf "s$i.bin" -f 2>&1 | tail -2
  if [ -f "s$i.bin" ]; then
    ls -la "s$i.bin" | awk '{print "  taille:", $5}'
    xxd "s$i.bin" | head -2
    echo "  --- dechiffrement AES-256-CBC (key+iv explicites) ---"
    openssl enc -d -aes-256-cbc -K $KEY -iv $IV -in "s$i.bin" -out "p$i.txt" 2>&1 | tail -2
    [ -f "p$i.txt" ] && { echo "  resultat:"; head -c 300 "p$i.txt"; echo; }
  fi
done
