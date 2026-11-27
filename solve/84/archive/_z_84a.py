import sys, json, re, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.6)
cy.login()
st, b = cy.req("GET", "/api/challenges/432/instance/")
d = json.loads(b) if b.startswith("{") else {}
print("=== 432 desc ===")
print(d.get("description"))
print("=== hints ===")
print(d.get("hints"))
B = pathlib.Path(r"/tmp/cylab_eps")
st, b = cy.req("GET", "/api/challenges/84/instance/")
d = json.loads(b) if b.startswith("{") else {}
desc = d.get("description") or ""
print("\n=== 84 desc ===")
print(desc[:300])
urls = [u for u in re.findall(r"https?://[^\s'\"<>]+", desc) if "challenge-files" in u]
for u in urls:
    name = u.rsplit("/", 1)[-1]
    dest = B / f"84_{name}"
    if not (dest.exists() and dest.stat().st_size > 500):
        r = requests.get(u, timeout=120, verify=False)
        dest.write_bytes(r.content)
        print("ok", name, len(r.content))
    else:
        print("deja", name, dest.stat().st_size)
