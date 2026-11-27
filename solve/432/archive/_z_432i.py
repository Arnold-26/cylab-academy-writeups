import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"/tmp/cylab_eps\432_modified.jpg"
d = open(p, "rb").read()
print("taille:", len(d))
idxs = [m.start() for m in re.finditer(rb"2023", d)]
print("occurrences de 2023:", len(idxs), idxs[:10])
for i in idxs[:6]:
    print("  @%d: %r" % (i, d[max(0,i-40):i+60]))
# chercher le format epoch-like ou un fuseau
for pat in (rb"\+01:00", rb"\.420", rb"21:46"):
    idxs2 = [m.start() for m in re.finditer(pat, d)]
    print(pat, "->", len(idxs2), idxs2[:5])
