import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/432/instance/?source=library")
desc = ""
for _ in range(15):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/432/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        if len(desc) > 50:
            break
print("=== DESC 432 ===")
print(desc[:1200])
open(r"D:\ctf-index\_z_432desc.txt", "w").write(desc)
