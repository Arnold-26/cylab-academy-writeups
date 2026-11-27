import sys, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:27114/"
s = requests.Session()
for path in ("api/report", "report"):
    for method in ("GET", "POST"):
        try:
            r = s.request(method, BASE + path, json={"url": BASE}, timeout=12)
            print("%-12s %-5s -> %d | %s" % (path, method, r.status_code, r.text[:160].replace("\n", " ")))
        except Exception as e:
            print(path, method, "ERR", type(e).__name__)
# verifier le contenu de index/designer pour un bouton report
t = requests.get(BASE + "designer.js", timeout=20).text
for kw in ("report", "admin", "flag", "localStorage", "location.href"):
    print("designer.js contient %-14s: %s" % (kw, kw in t))
