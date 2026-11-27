import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.set_int_max_str_digits(0)
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/107/instance/?source=library")
host = port = None
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/107/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(1), int(m.group(2))
        break
s = socket.create_connection((host, port), timeout=15)
s.settimeout(6)
out = b""
t0 = time.time()
while time.time() - t0 < 6:
    try:
        c = s.recv(65536)
        if not c:
            break
        out += c
    except socket.timeout:
        break
s.close()
txt = out.decode("latin-1", "replace").strip()
m = re.search(r"flag:\s*(\d+)", txt)
num = m.group(1)
print("digits:", len(num), "| bits:", int(num).bit_length())

def iroot3(x):
    lo, hi = 0, 1
    while hi ** 3 <= x:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** 3 <= x:
            lo = mid
        else:
            hi = mid
    return lo, lo ** 3 == x

print("essai cube root global:", end=" ")
r, exact = iroot3(int(num))
print("bits:", r.bit_length(), "| exact:", exact)
if exact:
    try:
        print("bytes:", r.to_bytes((r.bit_length() + 7) // 8, "big")[:200])
    except Exception as e:
        print("err", e)
# essai par blocs de longueurs candidates
for L in range(60, 240, 2):
    if len(num) % L:
        continue
    chunks = [num[i:i + L] for i in range(0, len(num), L)]
    chars = []
    ok = True
    for ch in chunks:
        v = int(ch)
        rr, ex = iroot3(v)
        if not ex or rr > 127:
            ok = False
            break
        chars.append(rr)
    if ok and chars:
        print("L=%d -> %r" % (L, bytes(chars)))
        break
