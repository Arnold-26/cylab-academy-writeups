import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=1.2)
cy.login()
try:
    cy.req("PUT", "/api/challenges/436/instance/?source=library")
    print("PUT ok")
except Exception as e:
    print("PUT err", e)
for i in range(20):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/436/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    print(i, d.get("status"), (d.get("description") or "")[:80].replace("\n", " "))
    if d.get("status") == "RUNNING":
        print("\nDESC:", (d.get("description") or ""))
        print("HINTS:", d.get("hints"))
        print("ENDPOINTS:", [(e.get("label"), e.get("endpoint")) for e in (d.get("endpoints") or [])])
        break
