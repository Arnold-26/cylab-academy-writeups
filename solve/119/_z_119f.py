import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image
out = [int(x) for x in open("/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/119_output.txt").read().split()]
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
    return "".join("1" if ((fun >> ((L - 1 - ys[i]) * 2)) & 3) == 3 else "0" for i in range(L))


grid = [unscramble(funs[i], seeds[i]) for i in range(N)]
print("exemple bloc 0:", grid[0])
print("exemple bloc 1:", grid[1])
# grille 30 x 264 : ligne (line*6 + b)
rows = []
for line in range(5):
    for b in range(6):
        rows.append("".join(grid[j][line * 6 + b] for j in range(N)))
print("lignes:", len(rows), "colonnes:", len(rows[0]))
img = Image.new("1", (N, 30))
px = img.load()
for y in range(30):
    for x in range(N):
        px[x, y] = 1 if rows[y][x] == "1" else 0
img.convert("L").resize((N * 5, 30 * 5), Image.NEAREST).save("/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/119_grid.png")
print("ecrit 119_grid.png")
# compte les transitions par ligne (indice de motif)
for y in range(30):
    r = rows[y]
    print(y, r[:80])
