#!/bin/bash
cd .
python3 -c "
open('in_bf.txt','w').write('\n'.join(['1','2','3']*3000)+'\n')
print('input lines', 9000)
"
timeout 60 gdb -nx -q -batch \
  -ex "set pagination off" \
  -ex "break *0x808ba5c" \
  -ex "run < in_bf.txt" \
  -ex "printf \"HIT vulnerable fgets, esp=%p\\n\", \$esp" \
  -ex "bt 3" \
  -ex "kill" ./_z_bizz 2>&1 | tail -15
