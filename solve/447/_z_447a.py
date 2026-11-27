import sys, re, json, time, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
urllib3.disable_warnings()
cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/447/instance/?source=library")
base = None
desc = ""
for _ in range(12):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/447/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    m = re.search(r"(https?://[A-Za-z0-9.\-]+:\d+)", desc)
    if m:
        base = m.group(1).rstrip("/") + "/"
        break
print("desc:", desc[:400].replace("\n", " "))
print("base:", base)
if base:
    try:
        r = requests.get(base, timeout=20)
        print("page:", r.status_code, len(r.text))
        print(r.text[:1500])
    except Exception as e:
        print("ERR", type(e).__name__)
