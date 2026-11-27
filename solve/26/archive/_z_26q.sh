#!/bin/bash
cd /tmp/cylab_eps/sstvall || exit 1
python3 - <<'PYEOF'
import sstv, wave, numpy as np
src = "/tmp/cylab_eps/26_message.wav"
w = wave.open(src, 'rb')
sr = w.getframerate()
raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
print("duree totale: %.2f s" % (len(raw)/sr))
WIN = 120  # secondes par fenetre
for start in (0, 20, 40, 60, 80, 100):
    a = int(start*sr); b = min(len(raw), int((start+WIN)*sr))
    seg = raw[a:b]
    if len(seg) < sr*30:
        continue
    got = 0
    for mn in ("SCOTTIE_1", "MARTIN_1", "ROBOT_36"):
        m = getattr(sstv.Mode, mn)
        try:
            imgs = sstv.decode(seg, sr, mode=m, header=True)
        except Exception as e:
            continue
        for i, img in enumerate(imgs):
            out = "win%03d_%s_%d.png" % (start, mn, i)
            img.save(out)
            print("start=%3ds %-10s -> %s %s" % (start, mn, img.size, out))
            got += 1
    if got == 0:
        print("start=%3ds : aucun decodage avec en-tete" % start)
PYEOF
ls *.png 2>/dev/null | grep win | head -12
