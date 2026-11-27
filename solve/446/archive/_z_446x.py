import sys, json, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=1.0)
cy.login()
st, b = cy.req("GET", "/api/challenges/446/instance/")
d = json.loads(b) if b.startswith("{") else {}
print("DESC COMPLET:")
print(d.get("description"))
print("\nENDPOINTS:", d.get("endpoints"))
