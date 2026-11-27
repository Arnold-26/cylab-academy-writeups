import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.5)
cy.login()
cy.req("PUT", "/api/challenges/185/instance/?source=library")
desc = ""
for _ in range(10):
    st, b = cy.req("GET", "/api/challenges/185/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    if "http" in desc or "nc " in desc:
        break
    time.sleep(0.4)
print(desc[:800])
print("\nendpoints:", d.get("endpoints"))
