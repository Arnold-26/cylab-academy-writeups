#!/bin/bash
cd /tmp/cylab_eps/sstvall || exit 1
python3 - <<'PYEOF'
import sstv, wave, numpy as np
src = "/tmp/cylab_eps/26_message.wav"
w = wave.open(src, 'rb')
sr = w.getframerate()
raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)

def metrics(img):
    a = np.asarray(img.convert('L'), dtype=float)
    contrast = a.std()
    black = float(np.mean(a < 12))
    shifts = []
    for y in range(1, a.shape[0]):
        prev, row = a[y-1], a[y]
        best, bs = -1e18, 0
        for s in range(0, 41):
            c = float(np.dot(prev[:320-s], row[s:])) if s else float(np.dot(prev, row))
            if c > best:
                best, bs = c, s
        shifts.append(bs)
    return contrast, black, float(np.mean(shifts)) if shifts else 99

results = []
for mode_name in ("SCOTTIE_1", "MARTIN_1", "ROBOT_36"):
    m = getattr(sstv.Mode, mode_name)
    for speed in [round(0.94 + 0.005*i, 3) for i in range(21)]:
        n = int(len(raw) / speed)
        idx = np.arange(n) * speed
        rs = np.interp(idx, np.arange(len(raw)), raw)
        try:
            imgs = sstv.decode(rs, sr, mode=m, header=True)
        except Exception:
            continue
        for i, img in enumerate(imgs):
            c, b, s = metrics(img)
            results.append((s + 100*b, c, b, s, mode_name, speed, i, img))
results.sort(key=lambda r: r[0])
for r in results[:8]:
    print("%-10s x%.3f idx%d | decalage=%.1f | contraste=%.1f | noir=%.2f" % (r[4], r[5], r[6], r[3], r[1], r[2]))
if results:
    sc, c, b, s, mn, sp, i, img = results[0]
    img.save("best2.png")
    print("sauve best2.png (%s x%.3f) %s" % (mn, sp, img.size))
PYEOF
