import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
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
print("cible:", host, port)
s = socket.create_connection((host, port), timeout=15)
s.settimeout(6)
out = b""
t0 = time.time()
while time.time() - t0 < 5:
    try:
        c = s.recv(65536)
        if not c:
            break
        out += c
    except socket.timeout:
        break
txt = out.decode("latin-1", "replace").strip()
m = re.search(r"flag:\s*(\d+)", txt)
n = int(m.group(1)) if m else None
print("bits du nombre:", n.bit_length() if n else None)
# essai d'interaction
for payload in (b"\n", b"hello\n"):
    try:
        s.sendall(payload)
        time.sleep(1.0)
        r = s.recv(4096)
        print("apres %r -> %r" % (payload[:6], r[:200]))
    except Exception as e:
        print("apres %r -> %s" % (payload[:6], type(e).__name__))
s.close()
