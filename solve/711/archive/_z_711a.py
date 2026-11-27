import sys, json, re, time, pathlib, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=1.2)
cy.login()
BASE = pathlib.Path(r"/tmp/cylab_711")
BASE.mkdir(exist_ok=True)
st, b = cy.req("GET", "/api/challenges/711/instance/")
d = json.loads(b) if b.startswith("{") else {}
desc = d.get("description") or ""
for u in [x for x in re.findall(r"https?://[^\s'\"<>]+", desc) if "challenge-files" in x]:
    name = u.rsplit("/", 1)[-1]
    dest = BASE / name
    r = requests.get(u, timeout=120, verify=False)
    dest.write_bytes(r.content)
    print("===", name, len(r.content))
    print(r.content.decode("utf-8", "replace")[:1200])
