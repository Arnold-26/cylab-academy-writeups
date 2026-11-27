import sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cid = int(sys.argv[1]) if len(sys.argv) > 1 else 478
cy = CyLab(delay=1.5)
cy.login()
st, b = cy.req("PUT", f"/api/challenges/{cid}/instance/?source=library")
print("PUT:", st, b[:300])
d = {}
for i in range(10):
    time.sleep(2)
    st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
    try:
        d = json.loads(b)
    except Exception:
        print(b[:200]); continue
    print(i, d.get("status"))
    if d.get("status") == "RUNNING":
        break
print(json.dumps({k: v for k, v in d.items() if k != 'description'}, indent=1)[:1500])
print("--- description ---")
print(d.get("description"))
