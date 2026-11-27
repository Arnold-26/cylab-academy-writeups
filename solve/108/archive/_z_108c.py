import sys, json, re, time, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
urllib3.disable_warnings()

cy = CyLab(delay=0.6)
cy.login()
cy.req("PUT", "/api/challenges/108/instance/?source=library")
base = None
for _ in range(12):
    time.sleep(1)
    st, b = cy.req("GET", "/api/challenges/108/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"(http://[A-Za-z0-9.\-]+:\d+/)", d.get("description") or "")
    if m:
        base = m.group(1)
        break
print("base:", base)
for attempt in range(8):
    try:
        r = requests.get(base, timeout=15)
        print("status:", r.status_code, "| len:", len(r.text), "| server:", r.headers.get("Server"))
        print(r.text[:1500])
        break
    except Exception as e:
        print("essai", attempt + 1, type(e).__name__)
        time.sleep(2)
