import sys, json, re, time, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=1.2)
cy.login()
FLAG = re.compile(r"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
cy.req("PUT", "/api/challenges/518/instance/?source=library")
url = None
desc = ""
for _ in range(25):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/518/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        cands = [c for c in re.findall(r"https?://[A-Za-z0-9.\-]+\.cylabacademy\.net(?::\d+)?", desc) if "challenge-files" not in c]
        if cands:
            url = cands[0]
            break
print("desc:", desc[:500].replace("\n", " "))
print("518:", url)
if url:
    base = url.rstrip("/")
    S = requests.Session()
    S.headers.update({"User-Agent": "Mozilla/5.0"})
    r = S.get(base, timeout=15, verify=False)
    print("page:", re.sub(r"\s+", " ", r.text or "")[:400])
    print("forms:", re.findall(r"<form[^>]*>", r.text or "")[:3])
    print("inputs:", re.findall(r'name=["\']([^"\']+)["\']', r.text or "")[:8])
    print("links:", re.findall(r'href=["\']([^"\']+)["\']', r.text or "")[:10])
