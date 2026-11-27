import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
st, b = cy.req("GET", "/api/challenges/387/instance/")
d = json.loads(b)
print("STATUS:", d.get("status"))
desc = d.get("description") or ""
print("LEN:", len(desc))
print(repr(desc))
