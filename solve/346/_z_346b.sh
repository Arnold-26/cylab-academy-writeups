#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
mkdir -p t346 && cd t346 || exit 1
cp ../346_game .
echo "academy{LOCAL_TEST_346}" > flag.txt
python3 -c "print('s'*25 + 'd'*85)" > moves.txt
wc -c moves.txt
echo "=== execution ==="
timeout 20 ./346_game < moves.txt 2>&1 | tail -8
