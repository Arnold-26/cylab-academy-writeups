#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
cp 39_need-for-speed 39_patched
python3 - <<'PYEOF'
p = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/39_patched"
d = bytearray(open(p,'rb').read())
off = 0x1314
print("avant:", d[off:off+5].hex())
assert d[off:off+5] == bytes.fromhex("e897fdffff"), "motif inattendu"
d[off:off+5] = b"\x90"*5
open(p,'wb').write(d)
print("apres:", d[off:off+5].hex())
PYEOF
chmod +x 39_patched
echo "=== execution patchee ==="
timeout 30 ./39_patched 2>&1 | head -20
