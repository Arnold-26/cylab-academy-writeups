import sys, json, re, time, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.7)
cy.login()
B = pathlib.Path(r"/tmp/cylab_eps")
st, b = cy.req("GET", "/api/challenges/133/instance/")
d = json.loads(b)
desc = d.get("description") or ""
print(desc[:600])
for u in re.findall(r"https?://[^\s'\"<>]+", desc):
    name = u.rsplit("/", 1)[-1]
    dest = B / f"133_{name}"
    if dest.exists() and dest.stat().st_size > 100:
        print("deja", dest.name, dest.stat().st_size)
        continue
    try:
        r = requests.get(u, timeout=90, verify=False, stream=True)
        n = 0
        with open(dest, "wb") as f:
            for chunk in r.iter_content(65536):
                f.write(chunk)
                n += len(chunk)
                if n > 30 * 1024 * 1024:
                    break
        print("ok", dest.name, n)
    except Exception as e:
        print("err", name, type(e).__name__)
