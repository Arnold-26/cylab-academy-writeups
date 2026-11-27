import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\13_investigative-reversing-2-encoded.bmp"
d = open(p, "rb").read()
bits = [b & 1 for b in d[:49 * 7]]
print("bits:", len(bits), "premiers:", bits[:21])
for order in ("lsb", "msb"):
    out = []
    for i in range(49):
        chunk = bits[i * 7:(i + 1) * 7]
        if order == "lsb":
            v = sum(bit << k for k, bit in enumerate(chunk))
        else:
            v = sum(bit << (6 - k) for k, bit in enumerate(chunk))
        out.append(chr(v) if 32 <= v < 127 else "?")
    s = "".join(out)
    print("%s -> %r" % (order, s))
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", s)
    if m:
        print("FLAG:", m.group(0))
# essai en sautant l'entete BMP (54 octets)
bits2 = [b & 1 for b in d[54:54 + 49 * 7]]
out = []
for i in range(49):
    chunk = bits2[i * 7:(i + 1) * 7]
    v = sum(bit << k for k, bit in enumerate(chunk))
    out.append(chr(v) if 32 <= v < 127 else "?")
print("apres entete ->", repr("".join(out)))
