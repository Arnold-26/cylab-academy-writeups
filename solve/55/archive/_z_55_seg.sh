#!/bin/bash
cd ./_z_55
# mapping fichier -> vaddr
python3 - <<'PY'
import subprocess, re
out = subprocess.run(['readelf','-lW','libc.so.6'], capture_output=True, text=True).stdout
print(out[:1200])
PY
