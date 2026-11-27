import sys, pathlib, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image
import numpy as np
p = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_iw/output.bmp"
im = Image.open(p).convert("RGB")
a = np.array(im)
print("shape:", a.shape)
FLAG = re.compile(rb"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
for bit in range(8):
    for ch, name in ((0, "R"), (1, "G"), (2, "B")):
        bits = ((a[:, :, ch] >> bit) & 1).flatten()
        n = len(bits) // 8 * 8
        bs = np.packbits(bits[:n]).tobytes()
        m = FLAG.search(bs)
        if m:
            print(f"FLAG bit={bit} canal={name}: {m.group(0).decode()}")
            sys.exit(0)
print("aucun flag dans les plans de bits")
# chercher aussi du texte lisible
for bit in (0, 1):
    bits = ((a[:, :, 0] >> bit) & 1).flatten()
    n = len(bits) // 8 * 8
    bs = np.packbits(bits[:n]).tobytes()
    txt = bs[:200]
    print(f"bit{bit} R debut: {txt[:60]!r}")
