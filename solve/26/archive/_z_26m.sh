#!/bin/bash
cd /tmp/cylab_eps/sstvall || exit 1
python3 - <<'PYEOF'
import sstv, wave, numpy as np
src = "/tmp/cylab_eps/26_message.wav"
w = wave.open(src, 'rb')
sr = w.getframerate()
raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)

def score(img):
    a = np.asarray(img.convert('L'), dtype=float)
    # pour chaque ligne, chercher le decalage (0..15) qui maximise la correlation avec la precedente
    shifts = []
    for y in range(1, min(a.shape[0], 60)):
        prev = a[y-1]
        row = a[y]
        best, bs = -1e18, 0
        for s in range(0, 16):
            if s == 0:
                c = float(np.dot(prev, row))
            else:
                c = float(np.dot(prev[:-s], row[s:]))
            if c > best:
                best, bs = c, s
        shifts.append(bs)
    return float(np.mean(shifts)) if shifts else 99.0

best = None
for mode_name in ("SCOTTIE_1", "MARTIN_1"):
    m = getattr(sstv.Mode, mode_name)
    for speed in [round(0.90 + 0.01*i, 2) for i in range(21)]:
        n = int(len(raw) / speed)
        idx = np.arange(n) * speed
        resampled = np.interp(idx, np.arange(len(raw)), raw)
        try:
            imgs = sstv.decode(resampled, sr, mode=m, header=True)
        except Exception:
            continue
        for i, img in enumerate(imgs):
            s = score(img)
            tag = "%s x%.2f idx%d" % (mode_name, speed, i)
            if best is None or s < best[0]:
                best = (s, tag, img)
            if s < 1.0:
                out = "straight_%s_%.2f_%d.png" % (mode_name, speed, i)
                img.save(out)
                print("BON %-22s score=%.2f -> %s" % (tag, s, out))
print("meilleur:", best[1] if best else None, "score=", best[0] if best else None)
if best:
    best[2].save("best.png")
    print("sauve: best.png", best[2].size)
PYEOF
