#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/sstvall || exit 1
python3 - <<'PYEOF'
import sstv, wave, numpy as np
src = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/26_message.wav"
w = wave.open(src, 'rb')
sr = w.getframerate()
data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
names = ['SCOTTIE_1','SCOTTIE_2','SCOTTIE_DX','MARTIN_1','MARTIN_2','ROBOT_36','ROBOT_72','PD_120','PD_180','PD_240']
for n in names:
    m = getattr(sstv.Mode, n)
    for hdr in (True, False):
        try:
            res = sstv.decode(data, sr, mode=m, header=hdr)
            for i, img in enumerate(res):
                out = "h%d_%s_%d.png" % (1 if hdr else 0, n, i)
                img.save(out)
                print("%-12s hdr=%-5s idx=%d taille=%s -> %s" % (n, hdr, i, img.size, out))
        except Exception as e:
            print("%-12s hdr=%-5s ERR %s" % (n, hdr, type(e).__name__))
PYEOF
ls -la *.png 2>/dev/null | wc -l
ls *.png 2>/dev/null | head -10
