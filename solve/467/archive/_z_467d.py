import sys, json, re, time, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/467/instance/?source=library")
base = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/467/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"http://([A-Za-z0-9.\-]+):(\d+)", d.get("description") or "")
        if m:
            base = m.group(0)
            break
print("base:", base)
if not base:
    sys.exit(0)
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
r = s.get(base + "/", timeout=20)
print("GET / ->", r.status_code, len(r.text))
print(r.text[:400])
for path in ("/impossibleLogin.php~", "/impossibleLogin.php", "/impossibleLogin.php.bak"):
    try:
        r2 = s.get(base + path, timeout=20)
        print("\n=== %s -> %s (%d o) ===" % (path, r2.status_code, len(r2.text)))
        print(r2.text[:900])
    except Exception as e:
        print(path, "ERR", type(e).__name__)
