import sys, hashlib, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
TARGET = "a0dbf9a811f074dd0697566da46543f1725fd8561ec3f4c422696dc846caea86"
names = [l.rstrip("\n") for l in (B / "474_cheese_list.txt").read_text(errors="replace").splitlines() if l.strip()]
hit = None
n = 0
for name in names:
    for i in range(256):
        salt = "%02x" % i
        for cand in (name + salt, salt + name):
            n += 1
            if hashlib.sha256(cand.encode()).hexdigest() == TARGET:
                hit = (name, salt, cand)
                break
        if hit:
            break
    if hit:
        break
print("essais:", n)
print("MATCH:", hit)
