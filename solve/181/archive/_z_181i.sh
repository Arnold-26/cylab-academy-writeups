#!/bin/bash
cd /tmp/cylab_eps || exit 1
printf '1\n2\nfizz\n' > /tmp/in181.txt
cat > /tmp/g181.py <<'PYEOF'
import gdb
gdb.execute("set pagination off")
gdb.execute("set confirm off")
gdb.execute("break *0x8049353")
gdb.execute("break *0x804930c")
n = 0
while n < 4:
    try:
        gdb.execute("continue")
    except gdb.error:
        break
    n += 1
    try:
        pc = int(gdb.parse_and_eval("$pc"))
    except Exception:
        break
    a = gdb.execute("x/s $esp", to_string=True).strip()
    b = gdb.execute("x/2s *(void**)$esp", to_string=True).strip()
    print("hit pc=0x%x" % pc)
    try:
        p1 = int(gdb.parse_and_eval("*(unsigned int*)$esp"))
        p2 = int(gdb.parse_and_eval("*(unsigned int*)($esp+4)"))
        print("  arg1:", gdb.execute("x/s 0x%x" % p1, to_string=True).strip())
        print("  arg2:", gdb.execute("x/s 0x%x" % p2, to_string=True).strip())
    except Exception as e:
        print("  err", e)
gdb.execute("quit")
PYEOF
gdb -nx -q -batch -x /tmp/g181.py ./181_vuln < /tmp/in181.txt 2>&1 | grep -vE "^1\? |^$" | head -25
