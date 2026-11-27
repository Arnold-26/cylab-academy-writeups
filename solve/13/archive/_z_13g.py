import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"/tmp/cylab_eps\13_investigative-reversing-2-encoded.bmp"
d = open(p, "rb").read()
start = 2000
bits = [b & 1 for b in d[start:start + 50 * 8]]
print("bits:", len(bits))
for order in ("lsb", "msb"):
    out = []
    for i in range(50):
        chunk = bits[i * 8:(i + 1) * 8]
        if order == "lsb":
            v = sum(bit << k for k, bit in enumerate(chunk))
        else:
            v = sum(bit << (7 - k) for k, bit in enumerate(chunk))
        out.append(v)
    raw = bytes((v) & 0xFF for v in out)
    plus5 = bytes(((v + 5) & 0xFF) for v in out)
    print("%s brut  : %r" % (order, raw))
    print("%s +5    : %r" % (order, plus5))
    for cand in (plus5, raw):
        m = re.search(rb"(?:academy|picoCTF)\{[^}]*\}", cand)
        if m:
            print("FLAG:", m.group(0).decode())
