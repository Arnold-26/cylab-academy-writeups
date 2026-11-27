import sys, zipfile, re, pathlib, base64
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"/tmp/cylab_eps\528_minions.apk")
z = zipfile.ZipFile(B)
pat = re.compile(rb"academy\{[^}\x00]{0,120}\}")
hits = []
for n in z.namelist():
    try:
        data = z.read(n)
    except Exception:
        continue
    for m in pat.finditer(data):
        hits.append((n, m.group(0).decode("utf-8", "replace")))
print("ACADEMY HITS:", len(hits))
for n, f in hits[:10]:
    print("  ", n, f)
print("\n=== assets / res/raw ===")
for n in z.namelist():
    if n.startswith("assets") or n.startswith("res/raw"):
        print("  %-50s %d" % (n, z.getinfo(n).file_size))
print("\n=== AndroidManifest (activites) ===")
try:
    mf = z.read("AndroidManifest.xml")
    for s in re.findall(rb"[ -~]{5,60}", mf)[:40]:
        print("  ", s.decode("utf-8", "replace"))
except Exception as e:
    print("ERR", e)
