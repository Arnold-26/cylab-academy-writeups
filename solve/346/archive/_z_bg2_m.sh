#!/bin/bash
cd /tmp/bg2
python3 -c "
import sys
sys.stdout.buffer.write(b'l'+b'y'+b'd'*47+b'w'*5)
" > in5.bin
rm -f out5.txt
timeout 10 ./_z_bg2 < in5.bin > out5.txt 2>&1
echo "exit=$?"
echo "--- flag in FILE (fully buffered) ? ---"
grep -a -n 'TESTFLAG' out5.txt && echo FOUND || echo "NO FLAG IN FILE"
echo "--- last 300 bytes ---"
tail -c 300 out5.txt | cat -v
