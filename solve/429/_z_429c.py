import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.6)
cy.login()
st, b = cy.req("GET", "/api/challenges/429/instance/")
d = json.loads(b)
print(d.get("description") or "(vide)")
print("\n--- hints:", d.get("hints"))
