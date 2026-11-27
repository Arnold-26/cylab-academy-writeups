import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=1.2)
cy.login()
cy.req("PUT", "/api/challenges/485/instance/?source=library")
for _ in range(15):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/485/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d+)", desc)
        print("nc:", m.group(0) if m else None, "|", (m.group(1), m.group(2)) if m else None)
        break
