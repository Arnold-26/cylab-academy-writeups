import sys, math
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
except ModuleNotFoundError:
    from Cryptodome.Cipher import AES
    from Cryptodome.Util.Padding import unpad

BLOCK = 16
UMAX = int(math.pow(256, BLOCK))
path = "/tmp/cylab_cr/76_body.enc.ppm"
data = open(path, "rb").read()
# entete PPM : 3 lignes
idx = 0
for _ in range(3):
    idx = data.index(b"\n", idx) + 1
header, body = data[:idx], data[idx:]
print("header:", header)
print("body:", len(body), "multiple de 16:", len(body) % 16 == 0)

blocks = [body[i:i + BLOCK] for i in range(0, len(body), BLOCK)]
print("nb blocs:", len(blocks))
# inverser l'addition : blocks[i+1] = (blocks[i] + blocks[i+1]) mod UMAX
dec = [blocks[0]]
for i in range(1, len(blocks)):
    prev = int(blocks[i - 1].hex(), 16)
    curr = int(blocks[i].hex(), 16)
    orig = (curr - prev) % UMAX
    dec.append(orig.to_bytes(BLOCK, "big"))
ct = b"".join(dec[1:])   # sans l'IV
print("ct len:", len(ct))
open("/tmp/aes_abc_ct.bin", "wb").write(ct)
print("ecrit /tmp/aes_abc_ct.bin")
