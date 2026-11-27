import socket, sys, time, re, json, itertools, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"D:\ctf-index\_z_107url.txt").read().split()
port = int(port)
s = socket.create_connection((host, port), timeout=20)
s.settimeout(2.5)

def readall(t=1.5):
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

bt = readall(3.0).decode("latin-1")
flag_ct = n = e = None
for ln in bt.split("\n"):
    if ln.startswith("flag: "):
        flag_ct = ln[6:].strip()
    elif ln.startswith("n: "):
        n = int(ln[3:].strip())
    elif ln.startswith("e: "):
        e = int(ln[3:].strip())
print("len(flag)=%d len(n)=%d" % (len(flag_ct), len(str(n))))

def enc(q):
    s.sendall(q.encode() + b"\n")
    r = readall(1.5).decode("latin-1")
    m = re.search(r"Here you go: (\d+)", r)
    return m.group(1) if m else None

qs = ["a", "x", "ax", "xa", "aa", "xx", "axa", "xax", "aax", "a"]
data = {}
for q in qs:
    data[q] = enc(q)
for q in qs:
    print("enc(%r) len=%d %s" % (q, len(data[q]), data[q][:20] + "..." + data[q][-12:]))

print("deterministic a:", data['a'] == data['a'])
W = len(str(n))

def splits(s_, k):
    """toutes les facons de couper s_ en k blocs de taille dans [W-3, W]"""
    res = []
    n_ = len(s_)
    def rec(i, k, cur):
        if k == 0:
            if i == n_:
                res.append(tuple(cur))
            return
        for w in (W, W - 1, W - 2, W - 3, W - 4):
            if i + w <= n_ and (n_ - (i + w)) >= 0:
                # borne grossiere
                if (n_ - (i + w)) <= (k - 1) * W and (n_ - (i + w)) >= (k - 1) * (W - 4):
                    cur.append(s_[i:i + w])
                    rec(i + w, k - 1, cur)
                    cur.pop()
    rec(0, k, [])
    return res

for q in ["ax", "xa", "aa", "xx"]:
    sp = splits(data[q], 2)
    print("%r : %d decoupages possibles" % (q, len(sp)))
    for x in sp:
        print("   ", x[0][:16], "... |", x[1][:16], "...")
json.dump(data, open(r"D:\ctf-index\_z_107_data2.json", "w"))
s.close()
