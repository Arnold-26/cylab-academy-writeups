import sys, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BIN = r"/tmp/cylab_eps\47_investigation-encoded-1-mystery"
OUT = r"/tmp/cylab_eps\47_investigation-encoded-1-output"
d = open(BIN, "rb").read()
# .rodata : vaddr 0x2000 == file offset 0x2000
secret = d[0x2020:0x2020 + 37]
matrix = struct.unpack("<54i", d[0x2060:0x2060 + 216])
print("secret:", secret.hex())
print("matrix (paires):", [(matrix[2 * i], matrix[2 * i + 1]) for i in range(12)], "...")


def bit(i):
    return (secret[i // 8] >> (7 - i % 8)) & 1


codes = {}
for k in range(27):
    ln, off = matrix[2 * k], matrix[2 * k + 1]
    if not (0 < ln < 20 and 0 <= off < 296):
        continue
    b = "".join(str(bit(off + j)) for j in range(ln))
    codes.setdefault(b, []).append(k)
print("\ncodes construits:", len(codes))

enc = open(OUT, "rb").read()
print("output:", len(enc), "octets")
bitstr = "".join(format(x, "08b") for x in enc)
print("bits:", len(bitstr))

for mapping in ("a+", "a-"):
    out = []
    i = 0
    ok = True
    while i < len(bitstr):
        matched = False
        for L in range(1, 20):
            if i + L > len(bitstr):
                break
            seg = bitstr[i:i + L]
            if seg in codes:
                ks = codes[seg]
                k = ks[0]
                ch = chr(ord("a") + k) if k < 26 else " "
                out.append(ch)
                i += L
                matched = True
                break
        if not matched:
            break
    print("\n[%s] decode: %r" % (mapping, "".join(out)[:200]))
