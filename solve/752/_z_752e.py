import sys, re, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:27165/"
s = requests.Session()
s.post(BASE + "signup", data={"username": "u752e", "email": "u752e@x.io", "password": "p752e"}, timeout=15)
s.post(BASE + "login", data={"username": "u752e", "password": "p752e"}, timeout=15)
r = s.get(BASE + "expenses", timeout=15)
print(r.text[:4000])
