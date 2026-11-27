import sys, zipfile, hashlib, pathlib, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"/tmp/cylab_eps")
z = zipfile.ZipFile(B / "56_b1g_mac.zip")
names = z.namelist()
print("entrees:", len(names))
for n in names:
    print("  ", n, z.getinfo(n).file_size)
print("\n=== md5 des fichiers (doublons ?) ===")
seen = {}
for n in names:
    if n.endswith("/"):
        continue
    h = hashlib.md5(z.read(n)).hexdigest()
    seen.setdefault(h, []).append(n)
for h, lst in seen.items():
    if len(lst) > 1:
        print("  identiques:", lst)
    else:
        print("  unique:", lst[0], h[:12])
