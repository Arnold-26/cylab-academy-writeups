import sys, re
import numpy as np
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = "/tmp/cylab_iw/output.bmp"
d = open(p, "rb").read()
import struct
offset = struct.unpack_from("<I", d, 10)[0]
w, h = 960, 540
arr = np.frombuffer(d[offset:offset + w * h * 4], dtype=np.uint8).reshape(h, w, 4)
FLAG = re.compile(rb"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
found = False
for ch, name in enumerate("BGRA"):
    chan = arr[:, :, ch].flatten()
    for bit in range(8):
        bits = ((chan >> bit) & 1)
        for off in range(8):
            b2 = bits[off:]
            n = len(b2) // 8 * 8
            for rev in (False, True):
                bs = np.packbits(b2[:n][::-1] if rev else b2[:n]).tobytes()
                m = FLAG.search(bs)
                if m:
                    print(f"FLAG canal={name} bit={bit} offset={off} rev={rev}: {m.group(0).decode()}")
                    found = True
                    sys.exit(0)
print("aucun flag trouve")
