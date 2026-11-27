import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps"
START, STRIDE, PER = 2019, 12, 10
out = []
for i in range(1, 6):
    d = open("%s\\54_Item0%d_cp.bmp" % (B, i), "rb").read()
    for k in range(PER):
        v = 0
        for j in range(8):
            v |= (d[START + STRIDE * k + j] & 1) << j
        out.append(v)
raw = bytes(out)
print("extrait (%d):" % len(raw), raw)
m = re.search(rb"(?:academy|picoCTF)\{[^}]*\}", raw)
print("FLAG:", m.group(0).decode() if m else None)
