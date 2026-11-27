import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"/tmp/cylab_eps\432_modified.jpg"
d = open(p, "rb").read()
old = b"2023:11:20 21:46:21.420+01:00"
new = b"1970:01:01 00:00:00.001+00:00"
print("ancienne len:", len(old), "| nouvelle len:", len(new), "| identiques:", len(old) == len(new))
i = d.find(old)
print("occurrence a:", i, "| total:", d.count(old))
if i >= 0 and len(old) == len(new):
    d2 = d.replace(old, new)
    open(p, "wb").write(d2)
    print("patch applique, taille:", len(d2))
else:
    # chercher des variantes
    for cand in (b"2023:11:20 21:46:21", b"TimeStamp", b"21:46:21"):
        j = d.find(cand)
        print("cherche", cand, "->", j)
