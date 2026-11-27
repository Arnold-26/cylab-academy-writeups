import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=1.2)
cy.login()
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/436/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        print("DESC:", desc[:600])
        print("HINTS:", d.get("hints"))
        print("ENDPOINTS:", [(e.get("label"), e.get("endpoint")) for e in (d.get("endpoints") or [])])
        break
else:
    print("pas demarre")
