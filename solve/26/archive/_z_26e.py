import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import sstv

path = "/tmp/cylab_m00n/message.wav"
try:
    img = sstv.decode_from_wav(path)
    out = "/tmp/cylab_m00n/decoded.png"
    img.save(out)
    print("ok:", out, img.size)
except Exception as e:
    print("err", type(e).__name__, e)
