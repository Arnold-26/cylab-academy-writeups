#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/t346 || exit 1
echo "=== 100 droite ==="
python3 -c "print('d'*100)" > m1.txt
timeout 10 ./346_game < m1.txt 2>&1 | grep -E "Player position|End tile|You win" | head -3
echo "=== 100 haut ==="
python3 -c "print('w'*100)" > m2.txt
timeout 10 ./346_game < m2.txt 2>&1 | grep -E "Player position|End tile|You win" | head -3
echo "=== 100 gauche ==="
python3 -c "print('a'*100)" > m3.txt
timeout 10 ./346_game < m3.txt 2>&1 | grep -E "Player position|End tile|You win" | head -3
echo "=== 100 bas ==="
python3 -c "print('s'*100)" > m4.txt
timeout 10 ./346_game < m4.txt 2>&1 | grep -E "Player position|End tile|You win" | head -3
