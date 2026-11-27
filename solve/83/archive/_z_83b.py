import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"/tmp/cylab_eps\83_investigative-reversing-3-encoded.bmp"
d = open(p, "rb").read()
START = 723
bits = [b & 1 for b in d[START:START + 100 * 8]]
print("bits:", len(bits))
for order in ("lsb", "msb"):
    vals = []
    for i in range(100):
        chunk = bits[i * 8:(i + 1) * 8]
        v = sum(bit << (k if order == "lsb" else 7 - k) for k, bit in enumerate(chunk))
        vals.append(v)
    # chaque caractere = 2 groupes identiques
    chars = []
    for i in range(50):
        chars.append(vals[i * 2])
    raw = bytes(chars)
    print("%s -> %r" % (order, raw))
    m = re.search(rb"(?:academy|picoCTF)\{[^}]*\}", raw)
    if m:
        print("FLAG:", m.group(0).decode())
    # variante : groupes consecutifs 0..49
    raw2 = bytes(vals[:50])
    print("   (0..49) -> %r" % raw2)
    m2 = re.search(rb"(?:academy|picoCTF)\{[^}]*\}", raw2)
    if m2:
        print("FLAG2:", m2.group(0).decode())
