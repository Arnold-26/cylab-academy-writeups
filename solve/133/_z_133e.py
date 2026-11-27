import sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
st, b = cy.req("PUT", "/api/challenges/133/instance/?source=library")
print("PUT ->", st, b[:300])
time.sleep(6)
st, b = cy.req("GET", "/api/challenges/133/instance/")
d = json.loads(b)
print("GET ->", d.get("status"), "| endpoints:", d.get("endpoints"))
