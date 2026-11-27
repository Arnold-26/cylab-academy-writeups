#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
mkdir -p t446 && cd t446 || exit 1
cp ../446_game game
echo "academy{TEST}" > flag.txt
echo "=== lancement (q puis w/a/s/d) ==="
printf 'ddddddddddddddddddd\n' | timeout 8 ./game 2>&1 | head -45
