#!/bin/bash
cd /tmp/cylab_eps/t346 || exit 1
echo "=== 4 x w puis 2720 x d ==="
python3 -c "
import sys
lines = ['w']*4 + ['d']*2720
sys.stdout.write('\n'.join(lines) + '\n')
" > oob1.txt
wc -l oob1.txt
timeout 60 ./346_game < oob1.txt > oob1.out 2>&1
echo "exit=$?"
tail -5 oob1.out | cat -v | head -8
grep -c "Player position" oob1.out
tail -3 oob1.out | grep -a "Player position"
