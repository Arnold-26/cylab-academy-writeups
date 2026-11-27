import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np
from PIL import Image

p = r"/tmp/cylab_eps\o141\evil_duck.png"
a = np.asarray(Image.open(p).convert("RGB")).astype(np.uint16)
by = (((a[:, :, 2] & 0xF) << 4) | (a[:, :, 1] & 0xF)).astype(np.uint8).ravel().tobytes()
print("total octets:", len(by))
# le script est du texte : prendre jusqu'au premier gros bloc non textuel
txt = by.decode("latin-1", "replace")
m = re.match(r"[ -~\r\n\t]{50,}", txt)
script = m.group(0) if m else txt[:2000]
print("longueur du script apparent:", len(script))
print("=== SCRIPT ===")
print(script[:2000])
open(r"/tmp/cylab_eps\o141\script.ps1", "w", encoding="utf-8").write(script)
print("\n=== recherche de flag / base64 ===")
for pat in (r"(?:academy|picoCTF)\{[^}]*\}", r"eyJ[A-Za-z0-9+/=]{20,}", r"[A-Za-z0-9+/]{40,}={0,2}"):
    for mm in re.finditer(pat, script):
        print("  ", pat[:20], "->", mm.group(0)[:160])
