import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
out = [int(x) for x in open("/tmp/cylab_eps/119_output.txt").read().split()]
N = len(out)
randoms = [((i * 327) % 681 + 344) % 313 for i in range(1, N + 1)]
seeds = [(i * 127) % 500 for i in range(1, N + 1)]
funs = []
prev = 0
for i in range(N):
    funs.append(out[i] ^ prev ^ randoms[i])
    prev = out[i]
L = 30


def perm(seed):
    bm = ["10"] * L
    ys = []
    for i in range(L):
        y = (i * seed) % L
        while bm[y] != "10":
            y = (y + 1) % L
        bm[y] = "XX"
        ys.append(y)
    return ys


def unscramble(fun, seed):
    ys = perm(seed)
    bits = []
    for i in range(L):
        y = ys[i]
        pair = (fun >> ((L - 1 - y) * 2)) & 0b11
        bits.append("1" if pair == 0b11 else "0")
    return "".join(bits)


grid = [unscramble(funs[i], seeds[i]) for i in range(N)]
# 5 lignes x 264 blocs de 6 bits -> 5 rangees de 1584 bits
rows = []
for line in range(5):
    bits = "".join(grid[j][line * 6:(line + 1) * 6] for j in range(N))
    rows.append(bits)
print("longueur de chaque ligne:", [len(r) for r in rows])
from PIL import Image
# essai 1 : 5 rangees de 1584
for w, h, name in ((1584, 5, "a"), (264, 30, "b"), (132, 60, "c"), (99, 80, "d")):
    bits = "".join(r[::-1] for r in rows) if False else "".join(rows)
    if len(bits) < w * h:
        continue
    b = bits[:w * h]
    img = Image.new("1", (w, h))
    px = img.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = 1 if b[y * w + x] == "1" else 0
    out_path = f"/tmp/cylab_eps/119_{name}.png"
    img.convert("L").resize((min(w * 8, 1600), min(h * 8, 1600)), Image.NEAREST).save(out_path)
    print("ecrit", out_path, w, h)
