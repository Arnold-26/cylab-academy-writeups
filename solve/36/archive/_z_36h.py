import sys, subprocess, struct, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BIN = r"/tmp/cylab_eps\36_no_auth_mistery"
OUT = r"/tmp/cylab_eps\36_investigation-encoded-2-output"
d = open(BIN, "rb").read()
va, off = 0x12e0, 0x12e0
secret = d[off + (0x1300 - va):off + (0x1300 - va) + 71]
idx_tab = list(struct.unpack("<38i", d[off + (0x1360 - va):off + (0x1360 - va) + 152]))
enc = open(OUT, "rb").read()


def bit(i):
    return (secret[i // 8] >> (7 - i % 8)) & 1


codes = {}
for ns in range(37):
    a, b = idx_tab[ns], idx_tab[ns + 1]
    if 0 <= a <= b <= len(secret) * 8:
        codes["".join(str(bit(i)) for i in range(a, b))] = ns
bitstr = "".join(format(x, "08b") for x in enc)
syms = []
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
    syms.append(hit[1])
    i += hit[0]
print("symboles:", syms)


def cvt(ns):
    if ns == 36:
        return " "
    c = (ns - 18) % 36
    return chr(ord("a") + c) if c < 26 else chr(ord("0") + (c - 26))


txt = "".join(cvt(s) for s in syms)
print("texte:", repr(txt))
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", m.group(0) if m else None)
for wrap in (txt, txt.rstrip(), txt.rstrip(" ")):
    if wrap:
        print("candidat academie: academy{%s}" % wrap.rstrip())
