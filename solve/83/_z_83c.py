import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\83_investigative-reversing-3-encoded.bmp"
d = open(p, "rb").read()
print("taille:", len(d), "| pixel offset:", int.from_bytes(d[10:14], "little"))


def extract(start, nc, order="lsb"):
    bits = [b & 1 for b in d[start:start + nc * 8]]
    if len(bits) < nc * 8:
        return b""
    out = []
    for i in range(nc):
        chunk = bits[i * 8:(i + 1) * 8]
        v = sum(bit << (k if order == "lsb" else 7 - k) for k, bit in enumerate(chunk))
        out.append(v)
    return bytes(out)


found = []
for start in range(0, min(len(d), 6000)):
    r = extract(start, 8)
    if r.startswith(b"academy{"):
        found.append(start)
print("offsets produisant 'academy{':", found[:10])
for st in found[:6]:
    txt = extract(st, 60)
    m = re.search(rb"(?:academy|picoCTF)\{[^}]*\}", txt)
    print("start", st, "->", txt[:70], "FLAG" if m else "")
    if m:
        print("FLAG:", m.group(0).decode())
        break
if not found:
    # essai avec le decalage i/2 (2 groupes par caractere)
    for start in range(0, min(len(d), 6000)):
        bits = [b & 1 for b in d[start:start + 50 * 16]]
        if len(bits) < 800:
            break
        vals = []
        for i in range(100):
            chunk = bits[i * 8:(i + 1) * 8]
            vals.append(sum(bit << k for k, bit in enumerate(chunk)))
        raw = bytes(vals[0::2])
        if raw.startswith(b"academy{"):
            print("offset (i/2) trouve:", start, raw[:70])
            break
