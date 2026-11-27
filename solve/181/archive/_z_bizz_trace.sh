#!/bin/bash
cd /tmp
cp ./_z_bizz_trace.gdb .
python3 -c "open('in.txt','w').write('x\n'*800)"
wc -l in.txt
timeout 150 gdb -q -batch -nx -x _z_bizz_trace.gdb ./_z_bizz 2>&1 | head -100
