import sys, zipfile, re, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\528_minions.apk")
z = zipfile.ZipFile(B)
pat = re.compile(rb"(academy|picoCTF)\{[^}\x00]{0,120}\}")
hits = []
for n in z.namelist():
    try:
        data = z.read(n)
    except Exception:
        continue
    for m in pat.finditer(data):
        hits.append((n, m.group(0).decode("utf-8", "replace")))
print("hits:", len(hits))
for n, f in hits[:20]:
    print("  %-40s %s" % (n, f))
# recherche de "flag" en clair dans les dex/assets
print("\n=== chaines contenant 'flag' dans les dex ===")
for n in z.namelist():
    if not (n.endswith(".dex") or n.startswith("assets") or n.startswith("res/raw")):
        continue
    data = z.read(n)
    for m in re.finditer(rb"[ -~]{6,60}", data):
        s = m.group(0)
        if b"flag" in s.lower() and len(s) < 80:
            print("  %-20s %s" % (n, s.decode("utf-8", "replace")))
