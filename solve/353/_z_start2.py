import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cid = int(sys.argv[1])
cy = CyLab(delay=1.5)
cy.login()
st, b = cy.req("PUT", f"/api/challenges/{cid}/instance/?source=library")
print("PUT:", st, b[:200])
for i in range(8):
    time.sleep(2)
    st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
    try:
        d = json.loads(b)
    except Exception:
        print(b[:200]); continue
    print(i, d.get("status"), "| desc:", (d.get("description") or "")[:600])
    if d.get("status") == "RUNNING":
        break
