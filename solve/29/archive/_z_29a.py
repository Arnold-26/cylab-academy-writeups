import sys, json, re, time, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=1.2)
cy.login()
FLAG = re.compile(r"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
cy.req("PUT", "/api/challenges/29/instance/?source=library")
url = None
for _ in range(15):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/29/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        cands = [c for c in re.findall(r"https?://[A-Za-z0-9.\-]+\.cylabacademy\.net(?::\d+)?", desc) if "challenge-files" not in c]
        if cands:
            url = cands[0]
            break
print("29:", url)
if url:
    base = url.rstrip("/")
    r = requests.get(base, timeout=15, verify=False)
    js = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", r.text or "", re.S))
    print("=== JS ===")
    print(js[:1500])
    rb = requests.get(base + "/bytes", timeout=15, verify=False)
    print("\n=== bytes ===")
    print((rb.text or "")[:200])
