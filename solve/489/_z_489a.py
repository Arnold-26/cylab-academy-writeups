import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/489/instance/?source=library")
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/489/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        print(d.get("description") or "")
        break
