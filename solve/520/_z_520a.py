import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/520/instance/?source=library")
time.sleep(5)
st, b = cy.req("GET", "/api/challenges/520/instance/")
d = json.loads(b) if b.startswith("{") else {}
desc = d.get("description") or ""
print("status:", d.get("status"))
print(desc[:600])
