import sys, json, re, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.6)
cy.login()
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
st, b = cy.req("GET", "/api/challenges/50/instance/")
d = json.loads(b) if b.startswith("{") else {}
desc = d.get("description") or ""
urls = [u for u in re.findall(r"https?://[^\s'\"<>]+", desc) if "challenge-files" in u]
for u in urls:
    name = u.rsplit("/", 1)[-1]
    dest = B / f"50_{name}"
    if not (dest.exists() and dest.stat().st_size > 300):
        r = requests.get(u, timeout=90, verify=False)
        dest.write_bytes(r.content)
        print("ok", name, len(r.content))
    else:
        print("deja", name, dest.stat().st_size)
