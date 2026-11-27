import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\432_original.jpg"
d = open(p, "rb").read()
print("taille:", len(d))
for pat in (rb"2023:11:20 15:46:23", rb"2023:11:20 21:46:21", rb"703", rb"TimeStamp", rb"2023"):
    idxs = [m.start() for m in re.finditer(pat, d)]
    print("%-26r -> %d occurrences %s" % (pat, len(idxs), idxs[:8]))
# contexte autour des 2023
for i in [m.start() for m in re.finditer(rb"2023", d)][:6]:
    print("  @%d %r" % (i, d[max(0, i - 20):i + 40]))
