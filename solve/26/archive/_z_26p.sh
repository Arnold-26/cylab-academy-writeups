#!/bin/bash
cd /tmp/cylab_eps/sstvall || exit 1
python3 - <<'PYEOF'
import sstv, wave, numpy as np
src = "/tmp/cylab_eps/26_message.wav"
w = wave.open(src, 'rb')
sr = w.getframerate()
raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)

def shear(img):
    a = np.asarray(img.convert('L'), dtype=float)
    ys = [y for y in range(a.shape[0]) if a[y].std() > 10]
    if len(ys) < 20:
        return 99.0
    y0 = ys[0]
    base = a[y0]
    shifts = []
    for y in ys[::8]:
        best, bs = -1e18, 0
        for s in range(-60, 61):
            if s >= 0:
                c = float(np.dot(base[:320-s], a[y][s:]))
            else:
                c = float(np.dot(base[-s:], a[y][:320+s]))
            if c > best:
                best, bs = c, s
        shifts.append((bs, y - y0))
    # regression lineaire du decalage en fonction de la ligne
    xs = np.array([d[1] for d in shifts], dtype=float)
    ys2 = np.array([d[0] for d in shifts], dtype=float)
    if xs.std() == 0:
        return 99.0
    slope = float(np.polyfit(xs, ys2, 1)[0])
    return slope * 100.0

cands = []
speeds = [round(1.0 + 0.001*i, 4) for i in range(-12, 13)]
for speed in speeds:
    n = int(len(raw) / speed)
    idx = np.arange(n) * speed
    rs = np.interp(idx, np.arange(len(raw)), raw)
    for mn in ("SCOTTIE_1",):
        m = getattr(sstv.Mode, mn)
        try:
            imgs = sstv.decode(rs, sr, mode=m, header=False)
        except Exception:
            continue
        for i, img in enumerate(imgs):
            s = shear(img)
            cands.append((abs(s), s, mn, speed, img))
cands.sort(key=lambda c: c[0])
for c in cands[:6]:
    print("%-10s x%.4f pente=%+.3f %%/ligne" % (c[2], c[3], c[1]))
if cands:
    img = cands[0][4]
    img.save("best4.png")
    print("sauve best4.png x%.4f" % cands[0][3])
PYEOF
