import socket, sys, time, re, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"./_z_107url.txt").read().split()
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
W = len(str(n))
print("len(flag)=%d W=%d" % (len(flag_ct), W))

def enc(q):
    s.sendall(q.encode() + b"\n")
    r = readall(1.5).decode("latin-1")
    m = re.search(r"Here you go: (\d+)", r)
    return m.group(1) if m else None

qs = ["a", "aa", "aaa", "aaaa", "ab", "aab", "aaab", "b", "ba", "abab", "x"]
d = {}
for q in qs:
    d[q] = enc(q)
    print("enc(%r) len=%d" % (q, len(d[q])))

print()
print("== tests de prefixe ==")
for q in ["aa", "aaa", "aaaa", "ab", "aab", "aaab", "ba", "abab"]:
    pre = d.get(q[:-1])
    if pre is None:
        continue
    val = d[q]
    print("%-6r len=%d : contient enc(%r) en prefixe: %s ; en suffixe: %s ; quelque part: %s"
          % (q, len(val), q[:-1], val.startswith(pre), val.endswith(pre), pre in val))

# compare blocks: decoupe le plus long en morceaux de W
def chunks(s_, k):
    out = []
    i = 0
    while i < len(s_):
        out.append(s_[i:i + W])
        i += W
    return out

print()
print("== decoupage naif en blocs de W ==")
for q in ["aa", "ab", "ba", "aaa", "aab"]:
    ch = chunks(d[q], W)
    print(q, [len(c) for c in ch], [c[:14] for c in ch])
print()
print("enc('a')[:20] =", d['a'][:20], " enc('a')[-12:] =", d['a'][-12:])
print("enc('b')[:20] =", d['b'][:20], " enc('b')[-12:] =", d['b'][-12:])
json.dump(d, open(r"./_z_107_data3.json", "w"))
open(r"./_z_107_flag3.txt", "w").write(flag_ct)
s.close()
