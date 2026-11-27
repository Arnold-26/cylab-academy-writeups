import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=1.0)
cy.login()
cy.req("PUT", "/api/challenges/386/instance/?source=library")
for _ in range(15):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/386/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        print("desc:", (d.get("description") or "")[:400])
        print("endpoints:", [(e.get("label"), e.get("endpoint")) for e in (d.get("endpoints") or [])])
        break
else:
    print("pas demarre")
