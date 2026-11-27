import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
for cid in (345, 346):
    cy.req("PUT", f"/api/challenges/{cid}/instance/?source=library")
    time.sleep(5)
    st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    print(f"\n=== {cid} {d.get('status')} ===")
    print(desc[:400])
