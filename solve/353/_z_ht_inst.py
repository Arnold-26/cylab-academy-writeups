import sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cid = int(sys.argv[1])
cy = CyLab(delay=1.5)
cy.login()
st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
print("GET:", st)
try:
    d = json.loads(b)
    print(json.dumps(d, indent=2)[:4000])
except Exception:
    print(b[:3000])
