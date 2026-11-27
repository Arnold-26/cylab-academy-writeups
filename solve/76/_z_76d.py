import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image

BLOCK = 16
UMAX = 1 << 128
path = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_cr/76_body.enc.ppm"
raw = open(path, "rb").read()
i = 0
for _ in range(3):
    i = raw.index(b"\n", i) + 1
header, body = raw[:i], raw[i:]
print("header:", header, "body:", len(body))
blocks = [body[k:k + BLOCK] for k in range(0, len(body), BLOCK)]
w, h = 1895, 820
for skip in (1, 0):
    dec = []
    prev = 0
    for b in blocks:
        curr = int.from_bytes(b, "big")
        new = (UMAX - prev + curr) % UMAX
        dec.append(new.to_bytes(BLOCK, "big"))
        prev = curr
    payload = b"".join(dec[skip:])
    img = Image.frombytes("RGB", (w, h), payload[:w * h * 3])
    out = f"/mnt/c/Users/arnol/AppData/Local/Temp/cylab_cr/dec_skip{skip}.png"
    img.save(out)
    print("ecrit:", out, img.size)
