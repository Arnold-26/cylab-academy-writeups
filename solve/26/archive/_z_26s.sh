#!/bin/bash
cd /tmp/cylab_eps/sstvall || exit 1
python3 - <<'PYEOF'
import sstv, wave, numpy as np
src = "/tmp/cylab_eps/26_message.wav"
w = wave.open(src, 'rb')
sr = w.getframerate()
raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)

def shear_slope(img):
    a = np.asarray(img.convert('L'), dtype=float)
    ys = [y for y in range(a.shape[0]) if a[y].std() > 10]
    if len(ys) < 20:
        return 99.0
    y0 = ys[0]; base = a[y0]
    pts = []
    for y in ys[::4]:
        best, bs = -1e18, 0
        for s in range(-80, 81):
            if s >= 0:
                c = float(np.dot(base[:320-s], a[y][s:]))
            else:
                c = float(np.dot(base[-s:], a[y][:320+s]))
            if c > best:
                best, bs = c, s
        pts.append((y - y0, bs))
    if len(pts) < 5:
        return 99.0
    xs = np.array([p[0] for p in pts], float); ys2 = np.array([p[1] for p in pts], float)
    return float(np.polyfit(xs, ys2, 1)[0]) * 100

cands = []
for speed in [0.919, 0.917, 0.921, 0.90, 0.93, 0.95, 0.97, 1.0]:
    n = int(len(raw) / speed)
    idx = np.arange(n) * speed
    rs = np.interp(idx, np.arange(len(raw)), raw)
    m = sstv.Mode.SCOTTIE_1
    try:
        imgs = sstv.decode(rs, sr, mode=m, header=False)
    except Exception as e:
        print("x%.3f ERR %s" % (speed, type(e).__name__)); continue
    for i, img in enumerate(imgs):
        s = shear_slope(img)
        print("x%.3f -> pente=%+.3f %%/ligne" % (speed, s))
        cands.append((abs(s), s, speed, img))
cands.sort(key=lambda c: c[0])
if cands:
    img = cands[0][3]
    img.save("final26.png")
    print("sauve final26.png x%.3f pente=%+.3f" % (cands[0][2], cands[0][1]))
PYEOF
