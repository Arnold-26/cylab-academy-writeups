#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/t346 || exit 1
echo "=== 20 deplacements 'w' (un par ligne) ==="
python3 -c "print('\n'.join(['w']*20))" > n1.txt
timeout 15 ./346_game < n1.txt 2>&1 | grep -E "Player position" | tail -3
echo "=== 20 deplacements 'a' ==="
python3 -c "print('\n'.join(['a']*20))" > n2.txt
timeout 15 ./346_game < n2.txt 2>&1 | grep -E "Player position" | tail -3
echo "=== 100 'w' ==="
python3 -c "print('\n'.join(['w']*100))" > n3.txt
timeout 30 ./346_game < n3.txt 2>&1 | grep -E "Player position" | tail -3
