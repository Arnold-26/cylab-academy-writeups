#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
mkdir -p t151 && cd t151 || exit 1
cp ../151_remote .
echo "academy{TESTFLAG}" > flag
echo "=== mot de passe forge ==="
printf 'aad[AAAAAAAAAAAA\n' | timeout 15 ./151_remote 2>&1 | head -10
echo "=== mauvais mot de passe (temoin) ==="
printf 'AAAAAAAAAAAAAAAA\n' | timeout 15 ./151_remote 2>&1 | head -10
