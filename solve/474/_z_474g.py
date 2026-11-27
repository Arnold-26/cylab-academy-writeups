import sys, hashlib, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"/tmp/cylab_eps")
TARGET = "a0dbf9a811f074dd0697566da46543f1725fd8561ec3f4c422696dc846caea86"
raw = [l.rstrip("\n") for l in (B / "474_cheese_list.txt").read_text(errors="replace").splitlines() if l.strip()]


def norms(n):
    return {n, n.lower(), n.upper(), n.title(),
            n.replace(" ", ""), n.lower().replace(" ", ""),
            n.replace("'", ""), n.lower().replace("'", ""),
            n.replace(" ", "_"), n.lower().replace(" ", "_"),
            n.strip(), n.lower().strip()}


hit = None
tries = 0
for n in raw:
    for name in norms(n):
        for i in range(256):
            for salt in ("%02x" % i, "%02X" % i):
                for cand in (name + salt, salt + name):
                    tries += 1
                    if hashlib.sha256(cand.encode()).hexdigest() == TARGET:
                        hit = (n, name, salt, cand)
                        break
                if hit:
                    break
            if hit:
                break
        if hit:
            break
    if hit:
        break
print("essais:", tries)
print("MATCH:", hit)
