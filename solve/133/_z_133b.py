import sys, json, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.7)
cy.login()
st, b = cy.req("GET", "/api/challenges/133/instance/")
d = json.loads(b)
print("status:", d.get("status"))
print("DESC COMPLETE:")
print(d.get("description") or "(vide)")
print("\nURLS:", re.findall(r"https?://[^\s'\"<>]+", d.get("description") or ""))
