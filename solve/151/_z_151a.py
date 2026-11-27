import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=1.0)
cy.login()
try:
    print(cy.req("PUT", "/api/challenges/151/instance/?source=library"))
except Exception as e:
    print("err", type(e).__name__)
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/151/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        print("desc:", desc[:600])
        print("nc:", re.findall(r"nc\s+[A-Za-z0-9.\-]+\s+\d+", desc))
        break
else:
    print("status:", d.get("status"))
