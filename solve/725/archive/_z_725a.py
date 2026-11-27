import sys, json, re, time, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/725/instance/?source=library")
base = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/725/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    if d.get("status") == "RUNNING" and desc:
        print("DESC:", desc[:500])
        m = re.search(r"http://([A-Za-z0-9.\-]+):(\d+)", desc)
        if m:
            base = m.group(0)
            break
print("base:", base)
if base:
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0"})
    r = s.get(base + "/", timeout=20)
    print("GET / ->", r.status_code, len(r.text))
    t = re.sub(r"<[^>]+>", " ", r.text)
    t = re.sub(r"\s+", " ", t)
    print(t[:500])
    print("\n=== form ===")
    for f in re.findall(r'<(?:input|form)[^>]*>', r.text):
        print("  ", f[:140])
