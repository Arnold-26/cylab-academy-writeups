import sys, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:27114/"
s = requests.Session()
for path in ("api/report", "report", "api/bot", "bot", "api/visit", "visit", "api/flag", "api/admin"):
    for method in ("GET", "POST"):
        try:
            r = s.request(method, BASE + path, json={"url": BASE}, timeout=10)
            body = r.text[:120].replace("\n", " ")
            print("%-12s %-5s -> %d %s" % (path, method, r.status_code, body))
        except Exception as e:
            print(path, method, "ERR", type(e).__name__)
