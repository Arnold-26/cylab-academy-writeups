import sys, hashlib, pathlib, itertools
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
TARGET = "a0dbf9a811f074dd0697566da46543f1725fd8561ec3f4c422696dc846caea86"
names = [l.rstrip("\n") for l in (B / "474_cheese_list.txt").read_text(errors="replace").splitlines() if l.strip()]
print("noms:", len(names))
variants = []
for n in names:
    variants.append((n, n))
    variants.append((n, n.lower()))
    variants.append((n, n.upper()))
    variants.append((n, n.replace(" ", "")))
    variants.append((n, n.replace(" ", "_")))
    variants.append((n, n.replace("'", "")))
    variants.append((n, n.strip()))
hit = None
for orig, v in variants:
    for algo in ("sha256", "md5", "sha1"):
        h = hashlib.new(algo, v.encode()).hexdigest()
        if h == TARGET:
            hit = (orig, v, algo)
            break
    if hit:
        break
print("MATCH:", hit)
