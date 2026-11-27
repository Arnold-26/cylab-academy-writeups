import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/352/instance/?source=library")
desc = ""
for _ in range(15):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/352/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        if "Username" in desc:
            break
print(desc)
open(r"D:\ctf-index\_z_352desc.txt", "w").write(desc)
