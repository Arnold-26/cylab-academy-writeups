import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/473/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/473/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", desc)
        if m:
            host, port = m.group(1), int(m.group(2))
            print("desc:", desc[:400])
            break
print("cible:", host, port)
if host:
    s = socket.create_connection((host, port), timeout=20)
    s.settimeout(8)
    time.sleep(0.5)
    out = b""
    try:
        out = s.recv(16384)
    except Exception:
        pass
    print("=== BANNIERE ===")
    print(out.decode("utf-8", "replace")[:1200])
    s.close()
