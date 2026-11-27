#!/bin/bash
cd /tmp/cylab_eps || exit 1
cat > /tmp/g151.py <<'PYEOF'
import gdb
gdb.execute("set pagination off")
gdb.execute("break *0x180f")
gdb.execute("run < /tmp/pw151.txt")
try:
    v = gdb.parse_and_eval("$rdi")
    print("RDI (valeur) = 0x%x = %d" % (int(v), int(v)))
except Exception as e:
    print("err", e)
gdb.execute("quit")
PYEOF
printf 'test\n' > /tmp/pw151.txt
gdb -nx -q -batch -x /tmp/g151.py ./151_remote 2>&1 | tail -12
