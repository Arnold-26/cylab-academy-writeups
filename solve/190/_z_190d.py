import sys, re, json, time, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
urllib3.disable_warnings()

cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/190/instance/?source=library")
base = None
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/190/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"(https?://[A-Za-z0-9.\-]+:\d+)", d.get("description") or "")
    if m:
        base = m.group(1).rstrip("/") + "/"
        break
print("base:", base)
s = requests.Session()
user = "hug%d" % (int(time.time() * 10) % 1000000)
r = s.post(base + "api/register", json={"user": user, "password": "pw190"}, timeout=25)
print("register:", r.status_code, r.text[:150], "| cookies:", list(s.cookies.keys()))
time.sleep(0.6)
for path in ("_/%s.git/api/readme?ref=refs/heads/master" % user,
             "_/%s.git/api/readme?ref=master" % user,
             "api/self"):
    try:
        r2 = s.get(base + path, timeout=25)
        print("=== %s -> %d" % (path[:60], r2.status_code))
        print("   ", r2.text[:400])
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r2.text)
        if m:
            print("FLAG:", m.group(0))
            break
    except Exception as e:
        print(path[:40], "ERR", type(e).__name__)
