import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\83_investigative-reversing-3-encoded.bmp"
d = open(p, "rb").read()
START = 723
STRIDE = 9
out = []
for k in range(50):
    v = 0
    for j in range(8):
        v |= (d[START + STRIDE * k + j] & 1) << j
    out.append(v)
raw = bytes(out)
print("brut:", raw)
for order in ("lsb",):
    print("flag candidat:", raw.decode("latin-1"))
m = re.search(rb"(?:academy|picoCTF)\{[^}]*\}", raw)
print("FLAG:", m.group(0).decode() if m else None)
# variante msb
out2 = []
for k in range(50):
    v = 0
    for j in range(8):
        v |= (d[START + STRIDE * k + j] & 1) << (7 - j)
    out2.append(v)
print("msb:", bytes(out2))
