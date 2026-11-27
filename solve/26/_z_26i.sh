#!/bin/bash
cd /tmp/cylab_eps || exit 1
mkdir -p sstvall && cd sstvall || exit 1
python3 - <<'PYEOF'
import sstv
src = "/tmp/cylab_eps/26_message.wav"
names = ['SCOTTIE_1','SCOTTIE_2','SCOTTIE_DX','MARTIN_1','MARTIN_2','ROBOT_36','ROBOT_72',
         'PD_50','PD_90','PD_120','PD_160','PD_180','PD_240','PD_290','PASOKON_P3','PASOKON_P5','PASOKON_P7']
for n in names:
    m = getattr(sstv.Mode, n)
    for hdr in (True, False):
        try:
            img, mode = sstv.decode_from_wav(src, mode=m, header=hdr)
            out = "h%d_%s.png" % (1 if hdr else 0, n)
            img.save(out)
            print("%-14s hdr=%-5s -> %s" % (n, hdr, img.size))
        except Exception as e:
            print("%-14s hdr=%-5s ERR %s" % (n, hdr, type(e).__name__))
PYEOF
ls -la *.png | head -8
