import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
out = [int(x) for x in open("/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/119_output.txt").read().split()]
N = len(out)
randoms = [((i * 327) % 681 + 344) % 313 for i in range(1, N + 1)]
seeds = [(i * 127) % 500 for i in range(1, N + 1)]
funs = []
prev = 0
for i in range(N):
    funs.append(out[i] ^ prev ^ randoms[i])
    prev = out[i]
print("fun[0..3]:", [hex(f) for f in funs[:4]])
print("out[0..3]:", [hex(o) for o in out[:4]])
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
        shift = (L - 1 - y) * 2
        pair = (fun >> shift) & 0b11
        bits.append("1" if pair == 0b11 else "0")
    return "".join(bits)


grid = [unscramble(funs[i], seeds[i]) for i in range(N)]
print("\nseeds[0..5]:", seeds[:6])
print("perm(seed0):", perm(seeds[0]))
print("\ngrid[0]:", grid[0])
print("grid[1]:", grid[1])
print("grid[2]:", grid[2])
print("grid[3]:", grid[3])
uniq = len(set(grid))
print("\nblocs uniques:", uniq, "/", N)
# distribution
from collections import Counter
print("plus frequents:", Counter(grid).most_common(3))
