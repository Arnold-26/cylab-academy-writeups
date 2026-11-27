#!/bin/bash
cd /tmp/cylab_eps || exit 1
python3 - <<'PYEOF'
import inspect, sstv
print("decode:", inspect.signature(sstv.decode))
print("decode_from_wav:", inspect.signature(sstv.decode_from_wav))
print("modes:", [m.name for m in sstv.Mode])
PYEOF
echo "=== decodage tous modes ==="
mkdir -p sstvall && cd sstvall || exit 1
python3 - <<'PYEOF'
import sstv, os
src = "/tmp/cylab_eps/26_message.wav"
for m in sstv.Mode:
    try:
        img, mode = sstv.decode_from_wav(src, m)
        out = "/tmp/cylab_eps/sstvall/%s.png" % m.name.replace(" ", "_")
        img.save(out)
        print("%-14s -> %s %s" % (m.name, img.size, out))
    except Exception as e:
        print("%-14s ERR %s" % (m.name, type(e).__name__))
PYEOF
