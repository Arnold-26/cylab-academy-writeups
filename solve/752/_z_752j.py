import sys, re, json, time, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
urllib3.disable_warnings()

cy = CyLab(delay=0.5)
cy.login()
cy.req("PUT", "/api/challenges/752/instance/?source=library")
base = None
for _ in range(12):
    time.sleep(0.9)
    st, b = cy.req("GET", "/api/challenges/752/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"(https?://[A-Za-z0-9.\-]+:\d+)", d.get("description") or "")
    if m:
        base = m.group(1).rstrip("/") + "/"
        break
print("base:", base)
s = requests.Session()
u = "o%d" % (int(time.time() * 3) % 100000)
try:
    r = s.post(base + "signup", data={"username": u, "email": u + "@x.io", "password": "pw"}, timeout=30)
    print("signup:", r.status_code)
    time.sleep(1.2)
    r = s.post(base + "login", data={"username": u, "password": "pw"}, timeout=30)
    print("login:", r.status_code, "| len:", len(r.text))
    time.sleep(1.2)
    for i in range(2):
        s.post(base + "expenses", data={"description": "e%d" % i, "amount": str(10 + i),
                                        "date": "2024-03-0%d" % (i + 1)}, timeout=30)
        time.sleep(1.2)
    r = s.get(base + "expenses", timeout=30)
    print("expenses:", r.status_code, len(r.text))
    print("liens:", re.findall(r'href="(/[^"]*\?[^"]*)"', r.text))
except Exception as e:
    print("ERR", type(e).__name__)
