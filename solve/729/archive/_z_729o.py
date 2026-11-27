import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
A = "http://xebec.cylabacademy.net:47074"
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
r = s.post(A + "/login.php", data={"username": "ctf-player", "password": "dyesebel"},
           timeout=20, allow_redirects=True)
print("login ->", r.status_code, "url:", r.url, len(r.text))
t = re.sub(r"<script.*?</script>", " ", r.text, flags=re.S)
t = re.sub(r"<[^>]+>", "\n", t)
t = html.unescape(t)
lines = [l.strip() for l in t.split("\n") if l.strip()]
for l in lines[:40]:
    print("  ", l[:180])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
print("\nFLAG dans la page:", f.group(0) if f else None)
