#!/bin/bash
cd ./_z_55
echo "=== one_gadget sur la libc fournie"
one_gadget libc.so.6 2>&1 | head -40
echo
echo "=== octets autour de __malloc_hook (0x3c4b10)"
python3 - <<'PY'
data = open('./_z_55/libc.so.6','rb').read()
for name, off in (("__malloc_hook",0x3c4b10), ("__free_hook",0x3c67a8)):
    print("---", name, hex(off))
    for start in range(off-0x40, off+0x10, 0x8):
        print("  %#x: %s" % (start, data[start:start+8].hex()))
PY
