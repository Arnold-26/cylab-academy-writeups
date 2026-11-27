import sys
import numpy as np
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = "/tmp/cylab_iw/output.bmp"
d = open(p, "rb").read()
import struct
offset = struct.unpack_from("<I", d, 10)[0]
w, h = 960, 540
arr = np.frombuffer(d[offset:offset + w * h * 4], dtype=np.uint8).reshape(h, w, 4)
for ch, name in enumerate("BGRA"):
    Image.fromarray(arr[:, :, ch]).save(f"/tmp/cylab_iw/chan_{name}.png")
    # LSB en image
    Image.fromarray(((arr[:, :, ch] & 1) * 255).astype(np.uint8)).save(f"/tmp/cylab_iw/lsb_{name}.png")
print("sauve")
