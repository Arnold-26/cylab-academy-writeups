import sys, os, hashlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
D = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/b1g/test"
files = sorted(os.listdir(D))
print("fichiers:", len(files))
for f in files:
    d = open(os.path.join(D, f), "rb").read()
    print(f"{f:22} {len(d):8} md5={hashlib.md5(d).hexdigest()[:12]}")
# comparer chaque paire
import itertools
seen = {}
for f in files:
    d = open(os.path.join(D, f), "rb").read()
    h = hashlib.md5(d).hexdigest()
    seen.setdefault(h, []).append(f)
print("\n=== groupes identiques ===")
for h, fs in seen.items():
    if len(fs) > 1:
        print(h[:10], fs)
# diff octet par octet entre Item01 et sa copie
a = open(os.path.join(D, "Item01.bmp"), "rb").read()
b = open(os.path.join(D, "Item01 - Copy.bmp"), "rb").read()
diffs = [i for i in range(min(len(a), len(b))) if a[i] != b[i]]
print("\nItem01 vs Copy: octets differents =", len(diffs), "premiers:", diff[:10] if False else diffs[:10])
