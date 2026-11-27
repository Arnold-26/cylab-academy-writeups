#!/bin/bash
cd /tmp/cylab_eps || exit 1
cat > /tmp/g151d.py <<'PYEOF'
import gdb
gdb.execute("set pagination off")
gdb.execute("set confirm off")
gdb.execute("set disable-randomization on")
gdb.execute("starti")
info = gdb.execute("info proc mappings", to_string=True)
base = None
for line in info.splitlines():
    parts = line.split()
    if len(parts) >= 6 and parts[-1].endswith("151_remote"):
        try:
            start = int(parts[0], 16); off = int(parts[3], 16)
        except ValueError:
            continue
        if off == 0:
            base = start
            break
print("base PIE =", hex(base) if base else None)
if base:
    gdb.execute("break *%d" % (base + 0x180f))
    gdb.execute("run < /tmp/pw151.txt")
    try:
        v = int(gdb.parse_and_eval("$rdi"))
        print("RDI = 0x%x = %d" % (v, v))
    except Exception as e:
        print("err", e)
gdb.execute("quit")
PYEOF
printf 'test\n' > /tmp/pw151.txt
gdb -nx -q -batch -x /tmp/g151d.py ./151_remote 2>&1 | tail -10
