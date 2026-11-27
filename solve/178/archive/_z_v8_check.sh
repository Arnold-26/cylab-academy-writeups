#!/bin/bash
echo "--- tools ---"
which nc ncat socat python3 curl 2>&1
python3 -c "import pwn; print('pwntools', pwn.__version__)" 2>&1 | tail -2
python3 -c "import struct; print('struct ok')"
echo "--- d8 sizes so far ---"
ls -la /tmp/v8/135 /tmp/v8/168 /tmp/v8/178
