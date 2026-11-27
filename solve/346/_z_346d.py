import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.4)
cy.login()
for cid in (346, 446):
    cy.req("PUT", f"/api/challenges/{cid}/instance/?source=library")
    desc = ""
    for _ in range(12):
        time.sleep(0.8)
        st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
        d = json.loads(b) if b.startswith("{") else {}
        desc = d.get("description") or ""
        if re.search(r"\d{2,5}", desc) and ("nc" in desc or "cylabacademy" in desc):
            break
    print("=== %d ===" % cid)
    print(desc.replace("\n", " ")[:600])
