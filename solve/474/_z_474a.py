import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/474/instance/?source=library")
time.sleep(6)
st, b = cy.req("GET", "/api/challenges/474/instance/")
d = json.loads(b) if b.startswith("{") else {}
print("status:", d.get("status"))
print((d.get("description") or "")[:600])
