import sys, re, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:27165/"
s = requests.Session()
s.post(BASE + "signup", data={"username": "u752d", "email": "u752d@x.io", "password": "p752d"}, timeout=15)
s.post(BASE + "login", data={"username": "u752d", "password": "p752d"}, timeout=15)
for path in ("dashboard", "expenses", "inbox"):
    r = s.get(BASE + path, timeout=15)
    print("=== /%s (%d, %d octets) ===" % (path, r.status_code, len(r.text)))
    txt = re.sub(r"<[^>]+>", " ", r.text)
    print(re.sub(r"\s+", " ", txt)[:450])
    for m in re.finditer(r"<form[^>]*>|<input[^>]*>|<select[^>]*>|<option[^>]*>|href=\"(/[^\"]*)\"", r.text):
        print("   ", m.group(0)[:120])
    print("   --- parametres GET dans les liens ---")
    for m in re.finditer(r"href=\"(/[^\"]*\?[^\"]*)\"", r.text):
        print("     ", m.group(1)[:100])
