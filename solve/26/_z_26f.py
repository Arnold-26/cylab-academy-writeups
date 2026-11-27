import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import sstv

path = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_m00n/message.wav"
imgs = sstv.decode_from_wav(path)
print("type:", type(imgs), "len:", len(imgs))
for i, img in enumerate(imgs):
    out = f"/mnt/c/Users/arnol/AppData/Local/Temp/cylab_m00n/img_{i}.png"
    img.save(out)
    print("ok:", out, img.size)
