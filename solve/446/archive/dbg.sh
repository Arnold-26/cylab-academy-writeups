#!/bin/bash
cd ./_z_446 || exit 1
python3 - <<'EOF'
from _z_446_solve import SEQ
open('/tmp/seq.bin','wb').write(SEQ)
print('seqlen', len(SEQ))
EOF
ls -l /tmp/seq.bin
gdb -nx -q -batch \
  -ex 'run < /tmp/seq.bin > /tmp/out.txt' \
  -ex 'printf "SIG=%d\n", $_siginfo' \
  -ex 'info registers eip ebp esp eax ebx ecx edx edi esi' \
  -ex 'x/10i $eip-10' \
  -ex 'bt' \
  --args ./game 2>&1 | tail -45
