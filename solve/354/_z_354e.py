import sys, struct, re
import numpy as np
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_iw/output.bmp"
d = open(p, "rb").read()
offset = struct.unpack_from("<I", d, 10)[0]
w, h = 960, 540
arr = np.frombuffer(d[offset:offset + w * h * 4], dtype=np.uint8).reshape(h, w, 4)
print("shape:", arr.shape)
FLAG = re.compile(rb"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
for ch, name in enumerate("BGRA"):
    chan = arr[:, :, ch]
    print(f"{name}: min={chan.min()} max={chan.max()} uniques={len(np.unique(chan))}")
    for bit in range(8):
        bits = ((chan >> bit) & 1).flatten()
        n = len(bits) // 8 * 8
        bs = np.packbits(bits[:n]).tobytes()
        m = FLAG.search(bs)
        if m:
            print(f"  FLAG bit={bit} canal={name}: {m.group(0).decode()}")
            sys.exit(0)
print("aucun flag")
