#!/bin/bash
cd /tmp/cylab_eps/g383 || exit 1
echo "=== steghide 7.bmp avec le mot de passe LoL ==="
rm -f s7.bin finallyReleased.txt
steghide extract -sf 7.bmp -p "yasuoaatroxashecassiopeia" -xf s7.bin -f 2>&1 | tail -3
if [ -f s7.bin ]; then
  echo "  taille: $(stat -c%s s7.bin)"
  echo "=== head hex ==="
  od -An -tx1 -N16 s7.bin
  echo "=== dechiffrement AES-256-CBC (sel 2350e88cbeaf16c9) ==="
  openssl enc -aes-256-cbc -d -S 2350e88cbeaf16c9 \
    -K a9f86b874bd927057a05408d274ee3a88a83ad972217b81fdc2bb8e8ca8736da \
    -iv 908458e48fc8db1c5a46f18f0feb119f -in s7.bin -out finallyReleased.txt 2>&1 | tail -3
  if [ -f finallyReleased.txt ]; then
    echo "=== contenu (extrait) ==="
    head -c 500 finallyReleased.txt
    echo
    echo "=== recherche du flag ==="
    grep -aoE "academy\{[^}]*\}|picoCTF\{[^}]*\}" finallyReleased.txt | head -5
  fi
fi
