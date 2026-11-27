#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
python3 - <<'PYEOF'
import sstv, traceback, wave
src = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/26_message.wav"
try:
    img, mode = sstv.decode_from_wav(src, mode=sstv.Mode.SCOTTIE_1)
    print("ok", img.size)
except Exception as e:
    print("ERREUR:", type(e).__name__, e)
    traceback.print_exc()
print("--- essai decode brut ---")
import numpy as np
w = wave.open(src, 'rb')
sr = w.getframerate()
data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
print("sr:", sr, "samples:", len(data), "duree:", len(data)/sr)
try:
    res = sstv.decode(data, sr, mode=sstv.Mode.SCOTTIE_1)
    print("decode ok:", type(res))
    if isinstance(res, tuple):
        print("  taille tuple:", len(res), [type(x) for x in res])
except Exception as e:
    print("decode ERREUR:", type(e).__name__, e)
PYEOF
