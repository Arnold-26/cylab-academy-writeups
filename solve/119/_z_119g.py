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
    return "".join("1" if ((fun >> ((L - 1 - ys[i]) * 2)) & 3) == 3 else "0" for i in range(L))


grid = [unscramble(funs[i], seeds[i]) for i in range(N)]
rows = []
for line in range(5):
    for b in range(6):
        rows.append("".join(grid[j][line * 6 + b] for j in range(N)))
allbytes = b""
for y in range(30):
    r = rows[y]
    by = bytes(int(r[i:i + 8], 2) for i in range(0, len(r) - 7, 8))
    print(f"ligne {y:2d}: {by}")
    allbytes += by
print("\n=== concatene ===")
print(allbytes[:400])
import re
m = re.search(rb"academy\{[^}]*\}", allbytes)
print("\nFLAG:", m.group(0).decode() if m else "non trouve")
# chercher aussi d'autres motifs
for mm in re.finditer(rb"[ -~]{10,}", allbytes):
    pass
