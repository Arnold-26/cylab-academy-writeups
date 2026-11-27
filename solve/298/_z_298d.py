import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=1.0)
cy.login()
print(cy.req("PUT", "/api/challenges/298/instance/?source=library"))
for _ in range(15):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/298/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        print("desc:", desc[:400])
        nc = re.findall(r"nc\s+[A-Za-z0-9.\-]+\s+\d+", desc)
        print("nc:", nc)
        st2, b2 = cy.req("GET", "/api/challenges/298/instance/")
        break
    print("status:", d.get("status"))
