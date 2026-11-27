import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/358/instance/?source=library")
time.sleep(5)
st, b = cy.req("GET", "/api/challenges/358/instance/")
d = json.loads(b) if b.startswith("{") else {}
desc = d.get("description") or ""
print(desc[:300])
m = re.search(r"http://([A-Za-z0-9.\-]+):(\d+)", desc)
with open(r"D:\ctf-index\_z_358url.txt", "w") as f:
    f.write(f"{m.group(1)} {m.group(2)}" if m else "")
print("URL:", m.group(0) if m else None)
