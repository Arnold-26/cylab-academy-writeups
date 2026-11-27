import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.5)
cy.login()
for cid in (108, 277, 344):
    cy.req("PUT", f"/api/challenges/{cid}/instance/?source=library")
    desc = ""
    for _ in range(8):
        st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
        d = json.loads(b) if b.startswith("{") else {}
        desc = d.get("description") or ""
        if "http" in desc or "nc " in desc:
            break
        time.sleep(0.4)
    print("=== %d %s ===" % (cid, d.get("status")))
    print(desc[:400])
    print()
