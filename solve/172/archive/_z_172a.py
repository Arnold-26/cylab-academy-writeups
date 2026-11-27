import sys, json, re, time, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.5)
cy.login()
B = pathlib.Path(r"/tmp/cylab_eps")
cy.req("PUT", "/api/challenges/172/instance/?source=library")
desc = ""
host = port = None
for _ in range(10):
    st, b = cy.req("GET", "/api/challenges/172/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", desc)
    if m and "challenge-files" in desc:
        host, port = m.group(2), int(m.group(3))
        break
    time.sleep(0.4)
print(desc[:400])
print("cible:", host, port)
for u in re.findall(r"https?://[^\s'\"<>]+", desc):
    name = u.rsplit("/", 1)[-1]
    dest = B / f"172_{name}"
    if dest.exists() and dest.stat().st_size > 100:
        print("deja", dest.name, dest.stat().st_size)
        continue
    try:
        r = requests.get(u, timeout=60, verify=False)
        dest.write_bytes(r.content)
        print("ok", dest.name, len(r.content))
    except Exception as e:
        print("err", name, type(e).__name__)
