import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/345/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/345/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)
seq = "w" * 4 + "a" * 8 + "s" * 29 + "d" * 93
s = socket.create_connection((host, port), timeout=25)
s.settimeout(8)
time.sleep(0.6)
banner = b""
try:
    banner = s.recv(65536)
except Exception:
    pass
print("=== banniere ===")
print(banner.decode("utf-8", "replace")[:400])
s.sendall(seq.encode())
time.sleep(4)
out = b""
try:
    while True:
        c = s.recv(65536)
        if not c:
            break
        out += c
except Exception as e:
    print("recv stop:", type(e).__name__)
print("=== suite ===")
print(out.decode("utf-8", "replace")[:800])
print("\nlongueur:", len(out))
s.close()
