#!/bin/bash
cd .
python3 -c "
lines=[]
for _ in range(500):
    lines += ['1','2','Fizz']
open('in_bf2.txt','w').write('\n'.join(lines)+'\n')
"
timeout 60 gdb -nx -q -batch \
  -ex "set pagination off" \
  -ex "break *0x808ba5c" \
  -ex "run < in_bf2.txt > /dev/null" \
  -ex "printf \"HIT\\n\"" \
  -ex "kill" ./_z_bizz 2>&1 | tail -6
