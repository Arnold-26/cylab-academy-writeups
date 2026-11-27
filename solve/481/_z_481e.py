import sys, pathlib, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image
import numpy as np
BASE = pathlib.Path("/mnt/c/Users/arnol/AppData/Local/Temp/cylab_z/481")
FLAG = re.compile(rb"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
files = sorted(BASE.glob("*.png"))
print("fichiers:", len(files))
for f in files:
    try:
        im = Image.open(f).convert("RGB")
        a = np.array(im)
    except Exception:
        continue
    for ch in range(3):
        lsb = (a[:, :, ch] & 1).flatten()
        n = len(lsb) // 8 * 8
        if n == 0:
            continue
        bs = np.packbits(lsb[:n]).tobytes()
        m = FLAG.search(bs)
        if m:
            print(f"FLAG dans {f.name} canal {ch}: {m.group(0).decode()}")
            sys.exit(0)
print("aucun flag LSB")
