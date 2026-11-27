#!/bin/bash
cd /tmp/cylab_eps/sstvall || exit 1
python3 - <<'PYEOF'
import sstv, wave, numpy as np
src = "/tmp/cylab_eps/26_message.wav"
w = wave.open(src, 'rb')
sr = w.getframerate()
raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
for speed in (0.945, 0.9447, 0.94, 0.96):
    n = int(len(raw) / speed)
    idx = np.arange(n) * speed
    rs = np.interp(idx, np.arange(len(raw)), raw)
    for hdr in (True, False):
        try:
            imgs = sstv.decode(rs, sr, mode=sstv.Mode.SCOTTIE_1, header=hdr)
        except Exception as e:
            print("x%.4f hdr=%s ERR %s" % (speed, hdr, type(e).__name__)); continue
        for i, img in enumerate(imgs):
            out = "d26_%.4f_%d_%d.png" % (speed, 1 if hdr else 0, i)
            img.save(out)
            print("x%.4f hdr=%-5s -> %s %s" % (speed, hdr, img.size, out))
PYEOF
ls d26_*.png 2>/dev/null
