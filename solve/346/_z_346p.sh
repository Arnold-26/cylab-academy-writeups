#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/t346 || exit 1
echo "=== local : w*4 + a*8 + p ==="
python3 -c "print('w'*4 + 'a'*8 + 'p')" > exp.txt
timeout 15 ./346_game < exp.txt 2>&1 | tail -6
echo "=== local : une ligne par mouvement ==="
python3 -c "
import sys
sys.stdout.write('\n'.join(list('w'*4 + 'a'*8 + 'p')) + '\n')
" > exp2.txt
timeout 15 ./346_game < exp2.txt 2>&1 | tail -6
