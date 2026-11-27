import sys, itertools
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


def unscramble(fun, seed, rev=False):
    ys = perm(seed)
    bits = []
    for i in range(L):
        y = ys[i]
        shift = (L - 1 - y) * 2
        pair = (fun >> shift) & 0b11
        bits.append("1" if pair == 0b11 else "0")
    if rev:
        bits = bits[::-1]
    return bits


def build(grid, chunk_order, bitrev, line_order):
    rows = []
    for line in line_order:
        bits = []
        for j in range(N):
            chunk = grid[j][line * 6:(line + 1) * 6]
            if bitrev:
                chunk = chunk[::-1]
            bits.extend(chunk)
        rows.append("".join(bits))
    return "".join(rows)


for bitrev in (False, True):
    for line_order in (list(range(5)), list(reversed(range(5)))):
        grid = [unscramble(funs[i], seeds[i]) for i in range(N)]
        data = build(grid, None, bitrev, line_order)
        by = bytes(int(data[i:i + 8], 2) for i in range(0, len(data) - 7, 8))
        printable = sum(1 for b in by if 32 <= b < 127)
        ratio = printable / max(len(by), 1)
        print(f"bitrev={bitrev} line_order={line_order[0]}.. : imprimable {ratio:.2%} | {by[:40]}")
        if ratio > 0.9:
            print("  >>>", by[:200])
