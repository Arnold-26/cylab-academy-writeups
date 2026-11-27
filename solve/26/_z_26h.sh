#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
python3 - <<'PYEOF'
import sstv, inspect
M = sstv.Mode
print("Mode members:", [a for a in dir(M) if not a.startswith('_')])
print("Mode init:", inspect.signature(M.__init__))
try:
    print("source partielle:", inspect.getsource(M)[:900])
except Exception as e:
    print("src err", e)
PYEOF
