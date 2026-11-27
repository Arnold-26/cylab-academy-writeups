import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/346/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/346/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)
s = socket.create_connection((host, port), timeout=25)
s.settimeout(8)
time.sleep(0.6)
banner = b""
try:
    banner = s.recv(65536)
except Exception:
    pass
print("banner:", banner.decode("utf-8", "replace")[:350])
# trouver la position de depart
m = re.search(rb"Player position: (-?\d+) (-?\d+)", banner)
print("depart:", m.groups() if m else None)
seq = "w" * 4 + "a" * 8 + "s" * 29 + "d" * 93
s.sendall((seq + "\n").encode())
found = None
tail = b""
t0 = time.time()
while time.time() - t0 < 50:
    try:
        c = s.recv(65536)
    except socket.timeout:
        break
    if not c:
        break
    tail = (tail + c)[-2500:]
    f = re.search(rb"(?:academy|picoCTF)\{[^}]*\}", c)
    if f:
        found = f.group(0).decode()
        break
print("FLAG:", found)
print("fin:", tail.decode("utf-8", "replace")[-400:])
s.close()
