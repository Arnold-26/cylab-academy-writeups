#!/bin/bash
cd /tmp/bg2
md5sum _z_bg2 game_dl ./_z_bg2 2>/dev/null
python3 - <<'EOF'
import sys
open('/tmp/bg2/in6.bin','wb').write(b'l'+b'y'+b'd'*47+b'w'*5+b'\n')
EOF
ls -l in6.bin
timeout 8 ./_z_bg2 < in6.bin > out6.txt 2>&1
echo "exit=$?"
echo -n "maps="; grep -a -c 'Player position' out6.txt
grep -a -o 'TESTFLAG[^}]*}' out6.txt || echo "NOFLAG"
tail -c 200 out6.txt | cat -v
echo
