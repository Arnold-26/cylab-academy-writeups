import sys, re, json, time, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
urllib3.disable_warnings()
cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/360/instance/?source=library")
base = None
desc = ""
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/360/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    m = re.search(r"(http://[A-Za-z0-9.\-]+:\d+/)", desc)
    if m:
        base = m.group(1)
        break
print("desc:", desc[:350].replace("\n", " "))
print("base:", base)
if base:
    for k in range(6):
        try:
            r = requests.get(base, timeout=15)
            print("status:", r.status_code, "| len:", len(r.text))
            print(r.text[:800])
            break
        except Exception:
            time.sleep(1.5)
