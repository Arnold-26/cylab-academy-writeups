import sys, re, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:27165/"
s = requests.Session()
for path in ("signup", "login"):
    r = s.get(BASE + path, timeout=15)
    print("=== /%s (%d) ===" % (path, r.status_code))
    for m in re.finditer(r"<form[^>]*>|<input[^>]*>", r.text):
        print("  ", m.group(0)[:130])
# inscription
r = s.post(BASE + "signup", data={"username": "u752a", "password": "p752a"}, timeout=15, allow_redirects=True)
print("signup ->", r.status_code, "| final:", r.url)
r = s.post(BASE + "login", data={"username": "u752a", "password": "p752a"}, timeout=15, allow_redirects=True)
print("login ->", r.status_code, "| final:", r.url)
txt = re.sub(r"<[^>]+>", " ", r.text)
print(re.sub(r"\s+", " ", txt)[:600])
print("=== liens/formulaires apres login ===")
for m in re.finditer(r"<form[^>]*>|<input[^>]*>|<a [^>]*href=\"[^\"]*\"", r.text):
    print("  ", m.group(0)[:130])
