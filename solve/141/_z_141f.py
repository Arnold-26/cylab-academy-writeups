import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
st, b = cy.req("GET", "/api/challenges/141/")
d = json.loads(b)
print("nom:", d.get("name"))
print("categorie:", (d.get("category") or {}).get("name"))
print("event:", (d.get("event") or {}).get("name"))
print("difficulte:", d.get("difficulty"), "| solves:", d.get("users_solved"))
