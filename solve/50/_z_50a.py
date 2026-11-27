import sys, json, re, requests, pathlib, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.6)
cy.login()
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
st, b = cy.req("GET", "/api/challenges/50/instance/")
d = json.loads(b) if b.startswith("{") else {}
print("status:", d.get("status"))
desc = d.get("description") or ""
print("desc:", desc[:400])
urls = [u for u in re.findall(r"https?://[^\s'\"<>]+", desc) if "challenge-files" in u]
for u in urls[:2]:
    name = u.rsplit("/", 1)[-1]
    dest = B / f"50_{name}"
    if not (dest.exists() and dest.stat().st_size > 300):
        r = requests.get(u, timeout=60, verify=False)
        dest.write_bytes(r.content)
        print("ok", name, len(r.content))
    else:
        print("deja", name, dest.stat().st_size)
if d.get("status") != "RUNNING":
    cy.req("PUT", "/api/challenges/50/instance/?source=library")
    time.sleep(6)
    st, b = cy.req("GET", "/api/challenges/50/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    print("apres PUT:", d.get("status"))
    print("desc:", (d.get("description") or "")[:400])
