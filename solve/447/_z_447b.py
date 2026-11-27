import sys, re, json, time, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
base = "http://xebec.cylabacademy.net:33257/"
# on relit l'instance pour l'URL exacte (elle change) -- on suppose que 447 vient d'etre cree
import json as J
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/447/instance/?source=library")
b447 = None
desc = ""
for _ in range(12):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/447/instance/")
    d = J.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    m = re.search(r"(https?://[A-Za-z0-9.\-]+:\d+)", desc)
    if m:
        b447 = m.group(1).rstrip("/") + "/"
        break
print("DESCRIPTION:", desc[:700])
print("base:", b447)
if b447:
    r = requests.get(b447 + "index.js", timeout=20)
    print("=== index.js ===", len(r.text))
    print(r.text[:6000])
