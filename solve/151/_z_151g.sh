#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
readelf -h 151_remote 2>/dev/null | grep -i entry
cat > /tmp/g151b.py <<'PYEOF'
import gdb
gdb.execute("set pagination off")
gdb.execute("starti")
pc = int(gdb.parse_and_eval("$pc"))
# l'entree est a l'offset lu dans readelf ; on determine la base en cherchant le mapping
info = gdb.execute("info proc mappings", to_string=True)
print(info[:400])
base = None
for line in info.splitlines():
    parts = line.split()
    if len(parts) >= 5 and parts[-1].endswith("151_remote"):
        start = int(parts[0], 16)
        off = int(parts[2], 16)
        base = start - off
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
gdb -nx -q -batch -x /tmp/g151b.py --args ./151_remote < /dev/null 2>&1 | tail -20
