import sys, json, re, time, pathlib, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=1.2)
cy.login()
BASE = pathlib.Path(r"/tmp/cylab_m00n")
BASE.mkdir(exist_ok=True)
try:
    cy.req("PUT", "/api/challenges/26/instance/?source=library")
except Exception:
    pass
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/26/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        print("desc:", desc[:300].replace("\n", " "))
        for u in [x for x in re.findall(r"https?://[^\s'\"<>]+", desc) if "challenge-files" in x]:
            name = u.rsplit("/", 1)[-1]
            dest = BASE / name
            if dest.exists() and dest.stat().st_size > 0:
                print("deja:", name, dest.stat().st_size)
                continue
            try:
                r = requests.get(u, timeout=180, verify=False)
                dest.write_bytes(r.content)
                print("ok:", name, len(r.content))
            except Exception as e:
                print("err", name, type(e).__name__)
        break
