import sys, re, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:27165/"
s = requests.Session()
r = s.post(BASE + "signup", data={"username": "u752b", "email": "u752b@x.io", "password": "p752b"},
           timeout=15, allow_redirects=True)
print("signup ->", r.status_code, "| final:", r.url)
r = s.post(BASE + "login", data={"username": "u752b", "password": "p752b"}, timeout=15, allow_redirects=True)
print("login ->", r.status_code, "| final:", r.url, "| len:", len(r.text))
txt = re.sub(r"<[^>]+>", " ", r.text)
print(re.sub(r"\s+", " ", txt)[:700])
print("=== liens/formulaires ===")
seen = set()
for m in re.finditer(r"<form[^>]*>|<input[^>]*>|href=\"([^\"]*)\"", r.text):
    g = m.group(0)[:130]
    if g not in seen:
        seen.add(g)
        print("  ", g)
