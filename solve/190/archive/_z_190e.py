import sys, re, json, time, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
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
# creer un repo normal pour verifier que la creation marche
user = "hg%d" % (int(time.time() * 7) % 1000000)
r = s.post(base + "api/register", json={"user": user, "password": "pw190"}, timeout=25)
print("register:", r.status_code, r.text[:120])
time.sleep(2.0)
print("self:", s.get(base + "api/self", timeout=20).text[:300])
r = s.post(base + "api/repo/create", json={"name": "myrepo", "initializeReadme": True}, timeout=25)
print("repo/create:", r.status_code, r.text[:200])
time.sleep(1.0)
print("self2:", s.get(base + "api/self", timeout=20).text[:400])
# tenter de lire le repo _/<user>
for p in ("_/%s.git/api/readme?ref=refs/heads/master" % user,):
    rr = s.get(base + p, timeout=20)
    print(p[:50], "->", rr.status_code, rr.text[:200])
