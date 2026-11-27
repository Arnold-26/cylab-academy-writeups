import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np
from PIL import Image

for name in ("evil_duck.png", "duck.png"):
    p = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\o141" + "\\" + name
    im = Image.open(p).convert("RGB")
    a = np.asarray(im)
    print("=====", name, a.shape, "=====")
    found = False
    for order in ("rgb", "bgr", "rb", "gr", "gb"):
        idx = {"r": 0, "g": 1, "b": 2}
        chans = [a[:, :, idx[c]] for c in order]
        for bit in range(3):
            bits = np.stack([(c >> bit) & 1 for c in chans], axis=-1).ravel()
            for step in (1, 2, 3, 4, 5, 6, 7, 8):
                b = bits[::step]
                n = (len(b) // 8) * 8
                if n < 80:
                    continue
                data = np.packbits(b[:n].reshape(-1, 8), axis=1).tobytes()
                for m in re.finditer(rb"[ -~]{12,}", data):
                    s = m.group(0)
                    if b"academy" in s or b"picoCTF" in s or b"{" in s and b"}" in s:
                        print("  ordre=%s bit=%d step=%d -> %r" % (order, bit, step, s[:120]))
                        found = True
    print("  trouve:", found)
