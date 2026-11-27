import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/529/instance/?source=library")
base = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/529/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"http://([A-Za-z0-9.\-]+):(\d+)", d.get("description") or "")
        if m:
            base = m.group(0)
            break
print("base:", base)
open(r"D:\ctf-index\_z_529base.txt", "w").write(base or "")
