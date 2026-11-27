#!/bin/bash
cd /tmp/cylab_eps/sstvall || exit 1
python3 - <<'PYEOF'
import sstv, wave, numpy as np
src = "/tmp/cylab_eps/26_message.wav"
w = wave.open(src, 'rb')
sr = w.getframerate()
raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)

def shear(img):
    """mesure la pente : decalage moyen (en px) entre la premiere et la derniere ligne"""
    a = np.asarray(img.convert('L'), dtype=float)
    rows = a.shape[0]
    ys = [y for y in range(rows) if a[y].std() > 10]
    if len(ys) < 10:
        return 99.0
    shifts = []
    ref = None
    for ti in [int(len(ys)*f) for f in (0.1, 0.3, 0.5, 0.7, 0.9)]:
        y = ys[ti]
        best, bs = -1e18, 0
        for s in range(-40, 41):
            prev = a[ys[0]]
            row = a[y]
            if s >= 0:
                c = float(np.dot(prev[:320-s], row[s:]))
            else:
                c = float(np.dot(prev[-s:], row[:320+s]))
            if c > best:
                best, bs = c, s
        shifts.append(bs / max(1, y - ys[0]))
    return float(np.mean(shifts)) * 100

cands = []
for speed in [0.88, 0.90, 0.905, 0.91, 0.915, 0.919, 0.925, 0.93, 0.94, 0.95, 1.0]:
    n = int(len(raw) / speed)
    idx = np.arange(n) * speed
    rs = np.interp(idx, np.arange(len(raw)), raw)
    for mn in ("SCOTTIE_1", "MARTIN_1"):
        m = getattr(sstv.Mode, mn)
        try:
            imgs = sstv.decode(rs, sr, mode=m, header=True)
        except Exception:
            continue
        for i, img in enumerate(imgs):
            s = shear(img)
            cands.append((abs(s), s, mn, speed, i, img))
            print("%-10s x%.3f idx%d pente=%.2f %%/ligne" % (mn, speed, i, s))
cands.sort(key=lambda c: c[0])
if cands:
    a, s, mn, sp, i, img = cands[0]
    img.save("best3.png")
    print("sauve best3.png (%s x%.3f) pente=%.2f" % (mn, sp, s))
PYEOF
