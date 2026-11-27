#!/bin/bash
cd /tmp/cylab_eps || exit 1
readelf -x .rodata 55_sice_cream 2>/dev/null | sed -n '20,60p'
echo "=== chaines lisibles du rodata ==="
python3 - <<'EOF'
d = open('55_sice_cream','rb').read()
# .rodata : chercher la section
import subprocess, re
out = subprocess.run(["readelf","-SW","55_sice_cream"], capture_output=True, text=True).stdout
for line in out.splitlines():
    if "] .rodata" in line:
        p = line.split()
        i = p.index(".rodata")
        va = int(p[i+2],16); off = int(p[i+3],16); sz = int(p[i+4],16)
        seg = d[off:off+sz]
        print("rodata va=%x off=%x size=%d" % (va,off,sz))
        for m in re.finditer(rb"[ -~]{3,}", seg):
            print("%x: %r" % (va+m.start(), m.group(0)))
        break
EOF
