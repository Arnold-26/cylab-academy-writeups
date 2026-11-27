import sys, math
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BLOCK = 16
UMAX = int(math.pow(256, BLOCK))
path = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_cr/76_body.enc.ppm"
data = open(path, "rb").read()
idx = 0
for _ in range(3):
    idx = data.index(b"\n", idx) + 1
header, body = data[:idx], data[idx:]
w, h = 1895, 820
blocks = [body[i:i + BLOCK] for i in range(0, len(body), BLOCK)]
dec = [blocks[0]]
for i in range(1, len(blocks)):
    prev = int(blocks[i - 1].hex(), 16)
    curr = int(blocks[i].hex(), 16)
    orig = (curr - prev) % UMAX
    dec.append(orig.to_bytes(BLOCK, "big"))
ct = b"".join(dec[1:])
# ecrire en PPM brut avec le header original
out = header + ct
outp = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_cr/dec.ppm"
open(outp, "wb").write(out)
print("ecrit:", outp, len(out))
# convertir en PNG pour visualisation
try:
    from PIL import Image
    im = Image.frombytes("RGB", (w, h), ct[:w * h * 3])
    im.save("/mnt/c/Users/arnol/AppData/Local/Temp/cylab_cr/dec.png")
    print("png ecrit")
except Exception as e:
    print("err png:", e)
