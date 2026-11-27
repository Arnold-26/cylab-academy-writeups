import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=1.0)
cy.login()
cy.req("PUT", "/api/challenges/446/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/446/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", desc)
        if m:
            host, port = m.group(1), int(m.group(2))
            print("nc:", host, port)
            break
print("connexion...")
try:
    s = socket.create_connection((host, port), timeout=15)
    s.settimeout(8)
    time.sleep(0.5)
    raw = b""
    try:
        raw = s.recv(65536)
    except Exception as e:
        print("recv err:", type(e).__name__)
    print("recu:", len(raw), "octets")
    print(repr(raw[:400]))
    s.close()
except Exception as e:
    print("connexion impossible:", type(e).__name__, e)
