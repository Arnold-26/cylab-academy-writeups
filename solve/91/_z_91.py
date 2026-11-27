import sys, json, re, requests, subprocess, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=1.2)
cy.login()
FLAG = re.compile(r"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
url = "https://challenge-files.cylabacademy.net/library/7a2d73afcf61879089df15c526cb7c833947dd7fa6aeb074eeacf4eb6a5ce096/flag.txt"
r = requests.get(url, timeout=60, verify=False)
print("contenu:", r.text[:500])
m = FLAG.search(r.text)
if m:
    f = m.group(0)
    print("FLAG:", f)
    st, b = cy.req("GET", "/api/challenges/91/")
    already = json.loads(b).get("solved_by_user")
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 91, "flag": f})
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print("91 ->", ok)
    if ok and not already:
        wu.write(91, "Nothing Up My Sleeve", "General Skills", "", "telechargement direct", f,
                 "Le fichier `flag.txt` est servi en clair sur le CDN : il suffit de le telecharger.")
