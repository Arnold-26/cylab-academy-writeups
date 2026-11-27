import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"/tmp/cylab_eps\pachinko\server\public\index.html"
t = open(p, encoding="utf-8", errors="replace").read()
print("taille:", len(t))
for kw in ("opcode", "instruction", "ISA", "nand", "circuit", "input1", "0x2000", "0x1000", "0x3000", "flag"):
    for m in list(re.finditer(kw, t, re.I))[:3]:
        seg = t[max(0, m.start()-120):m.start()+180]
        seg = re.sub(r"\s+", " ", seg)
        print("[%s] %s" % (kw, seg[:260]))
    print()
