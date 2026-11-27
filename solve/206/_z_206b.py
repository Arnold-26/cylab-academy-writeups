import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=1.2)
cy.login()
st, b = cy.req("GET", "/api/challenges/206/instance/")
d = json.loads(b) if b.startswith("{") else {}
print(json.dumps(d, indent=2, ensure_ascii=False)[:3000])
