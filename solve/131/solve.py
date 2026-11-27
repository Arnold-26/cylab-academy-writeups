# 131 - Some Assembly Required 2  (Web Exploitation, picoCTF 2021)
# Flag: academy{217f0babdae45710109bb2e6ac1b134a}
# Write-up: ../../../writeups/web-exploitation/131-some-assembly-required-2.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json, re, time, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=1.2)
cy.login()
cy.req("PUT", "/api/challenges/131/instance/?source=library")
url = None
for _ in range(15):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/131/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        print("desc:", desc[:300].replace("\n", " "))
        cands = [c for c in re.findall(r"https?://[A-Za-z0-9.\-]+\.cylabacademy\.net(?::\d+)?", desc) if "challenge-files" not in c]
        if cands:
            url = cands[0]
        break
print("131:", url)
if url:
    base = url.rstrip("/")
    r = requests.get(base, timeout=15, verify=False)
    print("page:", re.sub(r"\s+", " ", r.text or "")[:500])
    print("scripts:", re.findall(r'src=["\']([^"\']+)["\']', r.text or "")[:5])
    # recuperer le wasm
    for js in re.findall(r'src=["\']([^"\']+\.js)["\']', r.text or ""):
        rj = requests.get(base + "/" + js.lstrip("/"), timeout=15, verify=False)
        print(f"--- {js} ---")
        print((rj.text or "")[:400])
