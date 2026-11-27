import sys, re, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np
from PIL import Image

p = r"/tmp/cylab_eps\o141\evil_duck.png"
im = Image.open(p).convert("RGB")
a = np.asarray(im).astype(np.uint16)
h, w, _ = a.shape
print("dimensions:", w, h, "| pixels:", w * h)
for order in ("BG", "GB"):
    hi = a[:, :, 2] if order == "BG" else a[:, :, 1]
    lo = a[:, :, 1] if order == "BG" else a[:, :, 2]
    by = (((hi & 0xF) << 4) | (lo & 0xF)).astype(np.uint8).ravel()
    print("\n=== ordre %s : %d octets ===" % (order, len(by)))
    for endian in (">", "<"):
        L = struct.unpack(endian + "I", by[:4].tobytes())[0]
        ok = 0 < L <= len(by) - 4
        print("  entete%s = %d (coherent: %s)" % (endian, L, ok))
        if ok:
            payload = by[4:4 + L].tobytes()
            txt = payload.decode("utf-8", "replace")
            print("  extrait:", txt[:300].replace("\n", " ")[:300])
            open(r"/tmp/cylab_eps\o141\ps_%s%s.bin" % (order, "be" if endian == ">" else "le"), "wb").write(payload)
    # aussi tenter sans entete
    txt = by[:2000].tobytes().decode("latin-1", "replace")
    m = re.search(r"[ -~]{20,}", txt)
    print("  sans entete, texte initial:", (m.group(0)[:150] if m else "(rien)"))
