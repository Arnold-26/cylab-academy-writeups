import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=1.2)
cy.login()
st, b = cy.req("GET", "/api/challenges/725/instance/")
d = json.loads(b) if b.startswith("{") else {}
print(d.get("description") or "")
print("\nHINTS:")
for h in (d.get("hints") or []):
    print(" -", h)
print("\nENDPOINTS:")
for e in (d.get("endpoints") or []):
    print(" -", e)
