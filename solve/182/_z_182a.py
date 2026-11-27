import sys, re, json, time, requests, urllib3, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/182/instance/?source=library")
desc = ""
base = None
for _ in range(12):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/182/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    m = re.search(r"(https?://[A-Za-z0-9.\-]+:\d+)", desc)
    if m:
        base = m.group(1).rstrip("/") + "/"
        break
print("desc:", desc[:400].replace("\n", " "))
print("base:", base)
for u in re.findall(r"https?://[^\s'\"<>]+", desc):
    if "challenge-files" not in u:
        continue
    name = u.rsplit("/", 1)[-1]
    r = requests.get(u, timeout=60, verify=False)
    (B / f"182_{name}").write_bytes(r.content)
    print("   fichier:", name, len(r.content))
if base:
    try:
        r = requests.get(base, timeout=20)
        print("page:", r.status_code, len(r.text))
        for m in re.finditer(r"(src|href)=\"([^\"]+)\"", r.text):
            print("   ", m.group(2)[:80])
        print(r.text[:400])
    except Exception as e:
        print("ERR", type(e).__name__)
