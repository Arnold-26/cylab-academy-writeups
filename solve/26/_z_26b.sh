#!/bin/bash
cd /tmp/cylab_eps || exit 1
python3 - <<'PYEOF'
import wave
for f in ("26_message.wav", "28_message.wav"):
    try:
        w = wave.open(f, 'rb')
        n = w.getnframes(); sr = w.getframerate(); ch = w.getnchannels(); sw = w.getsampwidth()
        print("%s: %d frames, %d Hz, %d canaux, %d octets/echantillon, duree=%.2fs" % (f, n, sr, ch, sw, n/sr))
        w.close()
    except Exception as e:
        print(f, "ERR", e)
PYEOF
