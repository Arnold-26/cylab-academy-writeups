import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np
from PIL import Image

p = r"/tmp/cylab_eps\70_investigative-reversing-0-mystery.png"
a = np.asarray(Image.open(p).convert("RGB")).astype(np.uint8)
print("shape:", a.shape)
found = []
for order in ("rgb", "bgr", "rbg", "gbr", "brg", "grb"):
    idx = {"r": 0, "g": 1, "b": 2}
    chans = [a[:, :, idx[c]] for c in order]
    for bit in range(8):
        bits = np.stack([(c >> bit) & 1 for c in chans], axis=-1).ravel()
        for step in (1, 2, 3, 4, 8):
            b = bits[::step]
            n = (len(b) // 8) * 8
            if n < 100:
                continue
            data = np.packbits(b[:n].reshape(-1, 8), axis=1).tobytes()
            for m in re.finditer(rb"[ -~]{14,}", data):
                s = m.group(0)
                if any(k in s for k in (b"academy", b"picoCTF", b"flag", b"{")):
                    found.append((order, bit, step, s[:100]))
for f in found[:25]:
    print("  ordre=%s bit=%d step=%d -> %r" % f)
print("total:", len(found))
