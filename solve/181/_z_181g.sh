#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
cat > /tmp/ro181.py <<'PYEOF'
import subprocess, re
d = open('/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/181_vuln','rb').read()
out = subprocess.run(['readelf','-SW','/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/181_vuln'],
                     capture_output=True, text=True).stdout
for line in out.splitlines():
    if '] .rodata' in line:
        p = line.split(); i = p.index('.rodata')
        va = int(p[i+2],16); off = int(p[i+3],16); sz = int(p[i+4],16)
        seg = d[off:off+sz]
        print("rodata va=%x off=%x size=%d" % (va,off,sz))
        for m in re.finditer(rb'[ -~]{3,}', seg):
            print(hex(va+m.start()), m.group(0))
        break
PYEOF
python3 /tmp/ro181.py
