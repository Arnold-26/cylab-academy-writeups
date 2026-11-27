import sys, re, json, time, socket, math
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.5)
cy.login()
cy.req("PUT", "/api/challenges/379/instance/?source=library")
host = port = None
for _ in range(10):
    time.sleep(1)
    st, b = cy.req("GET", "/api/challenges/379/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(2), int(m.group(3))
        break
print("cible:", host, port)
s = socket.create_connection((host, port), timeout=15)
s.settimeout(8)
buf = b""
t0 = time.time()
while b"vainglory" not in buf and time.time() - t0 < 8:
    try:
        c = s.recv(4096)
        if not c:
            break
        buf += c
    except socket.timeout:
        break
txt = buf.decode("latin-1", "replace")
anger = int(re.search(r"anger\s*=\s*(\d+)", txt).group(1))
envy = int(re.search(r"envy\s*=\s*(\d+)", txt).group(1))
e = 65537
ed1 = e * envy - 1
print("c bits:", anger.bit_length(), "| ed1 bits:", ed1.bit_length())

flag_pt = None
for k in range(1, e):
    if ed1 % k:
        continue
    phi = ed1 // k
    if phi.bit_length() < 250 or phi.bit_length() > 260:
        continue
    n = phi
    for _ in range(200):
        s2 = n - phi + 1          # p+q suppose
        n2 = phi + 2 * math.isqrt(n) - 1
        if n2 == n:
            break
        n = n2
    # verification : discriminant carre
    s2 = n - phi + 1
    disc = s2 * s2 - 4 * n
    if disc < 0:
        continue
    r = math.isqrt(disc)
    if r * r != disc:
        continue
    p = (s2 + r) // 2
    q = (s2 - r) // 2
    if p * q != n:
        continue
    # dechiffrement
    pt = pow(anger, envy, n)
    try:
        cand = pt.to_bytes((pt.bit_length() + 7) // 8, "big").decode()
    except Exception:
        continue
    print("k=%d -> n=%d..." % (k, n % 100000))
    print("  plaintext candidat: %r" % cand)
    if re.fullmatch(r"[A-Za-z0-9]{1,20}", cand):
        flag_pt = cand
        print("PLAINTEXT:", cand)
        s.sendall(cand.encode() + b"\n")
        time.sleep(0.5)
        out = b""
        t0 = time.time()
        while time.time() - t0 < 5:
            try:
                cc = s.recv(4096)
                if not cc:
                    break
                out += cc
            except socket.timeout:
                break
        print("=== reponse ===")
        print(out.decode("latin-1", "replace")[:400])
        break
s.close()
