import sys, hashlib, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"/tmp/cylab_eps")
TARGET = "a0dbf9a811f074dd0697566da46543f1725fd8561ec3f4c422696dc846caea86"
names = [l.rstrip("\n") for l in (B / "474_cheese_list.txt").read_text(errors="replace").splitlines() if l.strip()]

sals = []
for i in range(10000):
    sals.append(str(i))
    sals.append("%02x" % i if i < 256 else format(i, "x"))
for i in range(0, 100, 1):
    sals.append("%02d" % i)
sals = list(dict.fromkeys(sals))
print("sels candidats:", len(sals), "| fromages:", len(names))
hit = None
n = 0
for name in names:
    for s in sals:
        for cand in (name + s, s + name):
            n += 1
            if hashlib.sha256(cand.encode()).hexdigest() == TARGET:
                hit = (name, s, cand)
                break
        if hit:
            break
    if hit:
        break
print("essais:", n)
print("MATCH:", hit)
