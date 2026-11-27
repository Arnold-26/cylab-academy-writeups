import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
stored = bytes.fromhex("037b7f780f0675153e0f1b694e0c0f78393d0a117e4d3d5810641050082a3a3b01102f16690710321f")


def swap_pairs(b):
    d = bytearray(b)
    for i in range(0, len(d) - 1, 2):
        d[i], d[i + 1] = d[i + 1], d[i]
    return bytes(d)


def step(i):
    x = i % 10
    x ^= 9 if i % 2 == 0 else 8
    x ^= 7 if i % 3 == 0 else (6 if i % 3 == 1 else 5)
    return x


def inverse(t):
    """inverse de : v ^= 20; v ^= d[i-1]; v ^= d[i-3]; v ^= step(i)  (lecture des valeurs finales voisines)"""
    d = bytearray(t)
    for i in range(len(d)):
        v = d[i]
        v ^= step(i)
        if i > 2:
            v ^= t[i - 3]
        if i > 0:
            v ^= t[i - 1]
        v ^= 20
        d[i] = v
    return bytes(d)


for label, cand in (("stored brut", stored),
                    ("perm(stored)", swap_pairs(stored))):
    r = inverse(cand)
    print("%-16s -> %s" % (label, "".join(chr(c) if 32 <= c < 127 else "." for c in r)))
    print("                 hex:", r.hex())
