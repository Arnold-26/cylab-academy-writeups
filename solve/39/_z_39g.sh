#!/bin/bash
cd /tmp/cylab_eps || exit 1
cp 39_need-for-speed 39_fast
python3 - <<'PYEOF'
p = "/tmp/cylab_eps/39_fast"
d = bytearray(open(p,'rb').read())
off = 0x1265
orig = bytes.fromhex("554889e5c745f87b05afe7c745fc00000000eb18")
print("avant:", d[off:off+len(orig)].hex())
assert d[off:off+len(orig)] == orig, "motif inattendu"
# prologue + mov eax, 0xe7af057b ; pop rbp ; ret  puis NOP
new = bytes.fromhex("554889e5b87b05afe75dc3")
d[off:off+len(new)] = new
for i in range(off+len(new), 0x129c):
    d[i] = 0x90
open(p,'wb').write(d)
print("apres:", d[off:off+len(new)].hex())
PYEOF
chmod +x 39_fast
echo "=== execution ==="
timeout 30 ./39_fast 2>&1 | head -20
