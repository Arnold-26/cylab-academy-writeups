import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = "/tmp/cylab_iw/output.bmp"
d = open(p, "rb").read()
print("taille:", len(d), "attendu:", 138 + 960*540*4)
print("trailing:", d[138+960*540*4:][:100])
asc = re.findall(rb"[ -~]{6,}", d[:200])
print("header strings:", asc[:10])
# chercher 'pico' ou 'academy' partout
for kw in (b"pico", b"academy", b"flag", b"steg"):
    i = d.lower().find(kw)
    print(kw, "->", i)
# convertir en PNG pour visualisation
import numpy as np
from PIL import Image
arr = np.frombuffer(d[138:138+960*540*4], dtype=np.uint8).reshape(540, 960, 4)
Image.fromarray(arr[:, :, [2, 1, 0]]).save("/tmp/cylab_iw/view.png")
print("sauve view.png")
