import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
out = [int(x) for x in open("/tmp/cylab_eps/119_output.txt").read().split()]
print("valeurs:", len(out), "bits max:", max(out).bit_length())
N = len(out)
randoms = [((i * 327) % 681 + 344) % 313 for i in range(1, N + 1)]
seeds = [(i * 127) % 500 for i in range(1, N + 1)]
print("randoms[0]:", randoms[0], "seeds[0]:", seeds[0])
# fun_i = result_i ^ result_{i-1} ^ randoms_i
funs = []
prev = 0
for i in range(N):
    f = out[i] ^ prev ^ randoms[i]
    funs.append(f)
    prev = out[i]
print("fun[0]:", funs[0], "bits:", funs[0].bit_length())
print("bits max des fun:", max(f.bit_length() for f in funs))

L = 30  # bits par bloc


def perm(seed):
    """rejoue la generation des indices y de Scramble"""
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
        # slot y occupe les 2 bits a la position (L-1-y)*2 dans la chaine de 60 bits
        shift = (L - 1 - y) * 2
        pair = (fun >> shift) & 0b11
        bits.append("1" if pair == 0b11 else "0")
    return "".join(bits)


grid = []  # 264 x 30
bad = 0
for i in range(N):
    s = unscramble(funs[i], seeds[i])
    if len(s) != 30:
        bad += 1
    grid.append(s)
print("blocs:", len(grid), "bits par bloc:", len(grid[0]))
# reconstruire : ligne l = bits l*6 .. l*6+5 de chaque bloc
rows = []
for line in range(5):
    bits = ""
    for j in range(N):
        bits += grid[j][line * 6:(line + 1) * 6]
    rows.append(bits)
data = ""
for r in rows:
    data += r
print("bits totaux:", len(data))
by = bytes(int(data[i:i + 8], 2) for i in range(0, len(data) - 7, 8))
print("octets:", len(by))
print(by[:200])
