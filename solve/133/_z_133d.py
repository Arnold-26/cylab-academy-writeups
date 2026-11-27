import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
st, b = cy.req("GET", "/api/challenges/133/instance/")
print("status http:", st)
d = json.loads(b)
print(json.dumps(d, indent=1)[:1200])
