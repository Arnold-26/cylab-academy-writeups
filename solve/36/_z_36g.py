import sys, subprocess, struct, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BIN = r"/tmp/cylab_eps\36_no_auth_mistery"
OUT = r"/tmp/cylab_eps\36_investigation-encoded-2-output"
d = open(BIN, "rb").read()
va, off = 0x12e0, 0x12e0


def get(addr, n):
    return d[off + (addr - va):off + (addr - va) + n]


secret = get(0x1300, 71)
idx_tab = list(struct.unpack("<38i", get(0x1360, 152)))
enc = open(OUT, "rb").read()


def make_codes(bitfn):
    c = {}
    for ns in range(37):
        a, b = idx_tab[ns], idx_tab[ns + 1]
        if not (0 <= a <= b <= len(secret) * 8):
            continue
        c["".join(str(bitfn(i)) for i in range(a, b))] = ns
    return c


def decode(codes, bitstr):
    res = []
    i = 0
    while i < len(bitstr):
        hit = None
        for L in range(1, 40):
            if i + L > len(bitstr):
                break
            if bitstr[i:i + L] in codes:
                hit = (L, codes[bitstr[i:i + L]])
                break
        if hit is None:
            break
        L, ns = hit
        res.append(ns)
        i += L
    return res


variants = {
    "msb": lambda i: (secret[i // 8] >> (7 - i % 8)) & 1,
    "lsb": lambda i: (secret[i // 8] >> (i % 8)) & 1,
}
maps = {
    "az09_": lambda ns: chr(ord("a") + ns) if ns < 26 else (chr(ord("0") + ns - 26) if ns < 36 else " "),
    "09az_": lambda ns: chr(ord("0") + ns) if ns < 10 else (chr(ord("a") + ns - 10) if ns < 36 else " "),
}
for vname, bf in variants.items():
    codes = make_codes(bf)
    for order in ("msb", "lsb"):
        bitstr = "".join(format(x, "08b") if order == "msb" else format(x, "08b")[::-1] for x in enc)
        syms = decode(codes, bitstr)
        for mname, mf in maps.items():
            txt = "".join(mf(s) for s in syms)
            print("%-4s %-4s %-6s -> %r" % (vname, order, mname, txt[:80]))
