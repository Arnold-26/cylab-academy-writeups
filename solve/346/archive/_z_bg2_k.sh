#!/bin/bash
cd /tmp/bg2
python3 -c "
import sys
sys.stdout.buffer.write(b'l'+b']'+b'd'*47+b'w'*5)
" > in3.bin
xxd in3.bin | head -4
rm -f out3.txt
timeout 10 ./_z_bg2 < in3.bin > out3.txt 2>&1
echo "exit=$?"
echo "--- flag in file? ---"
grep -a -n 'TESTFLAG' out3.txt || echo "NO FLAG IN FILE"
echo "--- last 200 bytes ---"
tail -c 200 out3.txt | cat -v
echo
echo "=== now with stdout to tty (script pty) ==="
rm -f out4.txt
timeout 10 script -qec "./_z_bg2 < in3.bin" /dev/null > out4.txt 2>&1
echo "exit=$?"
grep -a -n 'TESTFLAG' out4.txt || echo "NO FLAG (pty)"
echo "=== GNU_STACK ==="
readelf -l _z_bg2 | grep -A1 GNU_STACK
