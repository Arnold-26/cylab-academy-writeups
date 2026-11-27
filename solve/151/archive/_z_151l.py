import sys, hashlib, itertools, string
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PIECE = b"GpLaMjEW"
charset = string.ascii_letters + string.digits + "_{}-!@#$%^&*()+=,.;:?/<>[]|~"
found = []
for k in itertools.product(charset, repeat=4):
    key = "".join(k).encode()
    h = hashlib.md5(key + PIECE).digest()
    if h[0] == 0xC3:
        found.append("".join(k))
        print("TROUVE:", "".join(k), "digest:", h.hex())
        break
if not found:
    print("aucun dans ce charset")
