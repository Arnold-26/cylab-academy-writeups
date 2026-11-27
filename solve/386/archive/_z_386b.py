import sys, json, re, requests, pathlib, zipfile
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=1.0)
cy.login()
st, b = cy.req("GET", "/api/challenges/386/instance/")
d = json.loads(b) if b.startswith("{") else {}
desc = d.get("description") or ""
print("DESC COMPLET:")
print(desc)
B = pathlib.Path(r"/tmp/cylab_eps")
urls = [u for u in re.findall(r"https?://[^\s'\"<>]+", desc) if "challenge-files" in u]
for u in urls:
    name = u.rsplit("/", 1)[-1]
    dest = B / f"386_{name}"
    if not (dest.exists() and dest.stat().st_size > 500):
        r = requests.get(u, timeout=120, verify=False)
        dest.write_bytes(r.content)
        print("ok", name, len(r.content))
    if name.endswith(".zip"):
        z = zipfile.ZipFile(dest)
        print("contenu zip:", z.namelist()[:10])
