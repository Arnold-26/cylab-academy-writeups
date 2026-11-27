import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.7)
cy.login()
for cid in (760, 723):
    cy.req("PUT", f"/api/challenges/{cid}/instance/?source=library")
    time.sleep(5)
    st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    print(f"\n=== {cid} status={d.get('status')} ===")
    print((d.get("description") or "")[:900])
