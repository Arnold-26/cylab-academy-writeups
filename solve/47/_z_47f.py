import sys, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BIN = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\47_investigation-encoded-1-mystery"
OUT = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\47_investigation-encoded-1-output"
d = open(BIN, "rb").read()
secret = d[0x2020:0x2020 + 37]
matrix = struct.unpack("<54i", d[0x2060:0x2060 + 216])


def bit_msb(i):
    return (secret[i // 8] >> (7 - i % 8)) & 1


def bit_lsb(i):
    return (secret[i // 8] >> (i % 8)) & 1


enc = open(OUT, "rb").read()
for name, bf in (("msb", bit_msb), ("lsb", bit_lsb)):
    codes = {}
    for k in range(27):
        ln, off = matrix[2 * k], matrix[2 * k + 1]
        if not (0 < ln < 24 and 0 <= off < 296):
            continue
        b = "".join(str(bf(off + j)) for j in range(ln))
        codes.setdefault(b, k)
    for order in ("msb-first", "lsb-first"):
        if order == "msb-first":
            bitstr = "".join(format(x, "08b") for x in enc)
        else:
            bitstr = "".join(format(x, "08b")[::-1] for x in enc)
        for c0 in ("a", " "):
            out = []
            i = 0
            while i < len(bitstr):
                hit = None
                for L in range(1, 25):
                    if i + L > len(bitstr):
                        break
                    if bitstr[i:i + L] in codes:
                        hit = (L, codes[bitstr[i:i + L]])
                        break
                if hit is None:
                    break
                L, k = hit
                out.append(chr(ord(c0) + k) if (c0 == "a" and k < 26) else (" " if k == 26 else chr(ord(c0) + k)))
                i += L
            s = "".join(out)
            print("%-4s %-10s c0=%r -> %r  (reste %d bits)" % (name, order, c0, s[:120], len(bitstr) - i))
