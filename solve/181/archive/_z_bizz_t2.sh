#!/bin/bash
cd /tmp
cp ./_z_bizz_t2.gdb .
timeout 120 gdb -q -batch -nx -x _z_bizz_t2.gdb ./_z_bizz > /tmp/trace2.txt 2>&1
echo "trace lines: $(wc -l < /tmp/trace2.txt)"
grep -c "VULN REACHED" /tmp/trace2.txt
tail -5 /tmp/trace2.txt
