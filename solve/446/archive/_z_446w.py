import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=1.0)
cy.login()
print("PUT:", cy.req("PUT", "/api/challenges/446/instance/?source=library"))
for i in range(15):
    time.sleep(3)
    st, b = cy.req("GET", "/api/challenges/446/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d+)", desc)
    print(i, d.get("status"), (desc[:120] or "").replace("\n", " "), "| nc:", m.groups() if m else None)
    if m:
        break
