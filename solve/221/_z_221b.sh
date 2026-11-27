#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 221_matrix
echo 'rrrrrlrlrlrlrllddddddlddrrddrrrrdddrruuuruuuuuuurrddddddddlddrd' | timeout 30 ./221_matrix 2>&1 | tail -5
echo "--- essai 2 (variante) ---"
printf 'rrrrrlrlrlrlrllddddddlddrrddrrrrdddrruuuruuuuuuurrddddddddlddrd\n' | timeout 30 ./221_matrix 2>&1 | tail -5
