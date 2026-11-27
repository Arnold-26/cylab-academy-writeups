#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
cat > /tmp/g151c.py <<'PYEOF'
import gdb
gdb.execute("set pagination off")
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
    gdb.execute("continue")
    try:
        v = int(gdb.parse_and_eval("$rdi"))
        print("RDI = 0x%x = %d" % (v, v))
    except Exception as e:
        print("err", e)
gdb.execute("quit")
PYEOF
printf 'test\n' > /tmp/pw151.txt
gdb -nx -q -batch -x /tmp/g151c.py --args ./151_remote < /tmp/pw151.txt 2>&1 | tail -8
