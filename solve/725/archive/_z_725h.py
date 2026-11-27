import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/725/instance/?source=library")
url = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/725/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"http://([A-Za-z0-9.\-]+):(\d+)", d.get("description") or "")
        if m:
            url = m.group(0)
            break
print("URL:", url)
open(r"./_z_725url.txt", "w").write(url or "")
