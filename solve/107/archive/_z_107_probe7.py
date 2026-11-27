import socket, sys, time, re, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"./_z_107url.txt").read().split()
port = int(port)
s = socket.create_connection((host, port), timeout=30)
s.settimeout(4)

def readall(t=2.0):
    out = b""
    end = time.time() + t
    while time.time() < end:
        try:
            d = s.recv(65536)
        except socket.timeout:
            break
        if not d:
            break
        out += d
    return out

bt = readall(4.0).decode("latin-1")
flag_ct = n = e = None
for ln in bt.split("\n"):
    if ln.startswith("flag: "):
        flag_ct = ln[6:].strip()
    elif ln.startswith("n: "):
        n = int(ln[3:].strip())
    elif ln.startswith("e: "):
        e = int(ln[3:].strip())
W = len(str(n))
print("len(flag)=%d W=%d" % (len(flag_ct), W))

def enc(q, tries=2):
    for _ in range(tries):
        s.sendall(q.encode() + b"\n")
        r = readall(2.0).decode("latin-1")
        m = re.search(r"Here you go: (\d+)", r)
        if m:
            return m.group(1)
    return None

qs = ["a", "aa", "aaa", "ab", "b", "ba", "1", "11", "12"]
d = {}
for q in qs:
    v = enc(q)
    d[q] = v
    print("enc(%r) -> %s" % (q, ("len=%d" % len(v)) if v else "ECHEC"))

print("\n=== relations exactes ===")
def rel(x, y):
    a, b = d.get(x), d.get(y)
    if not a or not b:
        return
    print("enc(%r) vs enc(%r): prefixe=%s suffixe=%s sous-chaine=%s  (len %d, %d)"
          % (x, y, b.startswith(a), b.endswith(a), a in b, len(a), len(b)))
rel("a", "aa"); rel("a", "aaa"); rel("aa", "aaa")
rel("a", "ab"); rel("b", "ab"); rel("b", "ba"); rel("a", "ba")
rel("1", "11"); rel("1", "12")
print()
for q in qs:
    if d.get(q):
        print("%-5r len=%3d debut=%s fin=%s" % (q, len(d[q]), d[q][:26], d[q][-18:]))
json.dump({"flag": flag_ct, "n": str(n), "e": e, "d": d}, open(r"./_z_107_data4.json", "w"))
s.close()
