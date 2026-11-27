#!/bin/bash
cd /tmp/cylab_eps || exit 1
printf 'test\n' > /tmp/pw151.txt
gdb -nx -q -batch -ex "set pagination off" -ex "run < /tmp/pw151.txt" -ex "bt" -ex "info registers rip rsp" ./151_remote 2>&1 | tail -20
