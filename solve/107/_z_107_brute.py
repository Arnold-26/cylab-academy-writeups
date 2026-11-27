import re, sys, itertools, string, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.set_int_max_str_digits(0)

txt = open(r"D:\ctf-index\_z_107_banner.txt", encoding="utf-8").read()
F = int(re.search(r"flag:\s*(\d+)", txt).group(1))
n = int(re.search(r"n:\s*(\d+)", txt).group(1))
e = int(re.search(r"e:\s*(\d+)", txt).group(1))

chunks = []
x = F
while x:
    chunks.append(x % n)
    x //= n
print("chunks:", len(chunks), flush=True)

alpha = (string.ascii_lowercase + string.digits + "_{}!" + string.ascii_uppercase + "-").encode()

for w in (1, 2):
    t0 = time.time()
    out = []
    ok = 0
    for c in chunks:
        got = None
        for tup in itertools.product(alpha, repeat=w):
            p = int.from_bytes(bytes(tup), "big")
            if pow(p, e, n) == c:
                got = bytes(tup).decode()
                break
        out.append(got if got else "?")
        ok += 1 if got else 0
    print("width", w, "matched", ok, "/", len(chunks), "%.1fs" % (time.time() - t0))
    print("  ", "".join(out))
