import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"/tmp/cylab_eps\13_investigative-reversing-2-encoded.bmp"
d = open(p, "rb").read()
for start in (1078, 1074, 1082, 54):
    bits = [b & 1 for b in d[start:start + 49 * 7]]
    if len(bits) < 49 * 7:
        continue
    for order in ("lsb", "msb"):
        out = []
        for i in range(49):
            chunk = bits[i * 7:(i + 1) * 7]
            v = sum(bit << (k if order == "lsb" else 6 - k) for k, bit in enumerate(chunk))
            out.append(chr(v) if 32 <= v < 127 else "?")
        s = "".join(out)
        print("start=%-5d %s -> %r" % (start, order, s))
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", s)
        if m:
            print("FLAG:", m.group(0))
