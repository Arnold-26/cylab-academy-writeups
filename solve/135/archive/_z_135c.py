import sys, json, re, time, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.7)
cy.login()
B = pathlib.Path(r"/tmp/cylab_eps")
st, b = cy.req("GET", "/api/challenges/135/instance/")
d = json.loads(b)
desc = d.get("description") or ""
urls = re.findall(r"https?://[^\s'\"<>]+", desc)
print("urls:", len(urls))
for u in urls:
    name = u.rsplit("/", 1)[-1]
    dest = B / f"135_{name}"
    if dest.exists() and dest.stat().st_size > 50:
        print("deja", dest.name, dest.stat().st_size)
        continue
    try:
        r = requests.get(u, timeout=60, verify=False, stream=True)
        n = 0
        with open(dest, "wb") as f:
            for chunk in r.iter_content(65536):
                f.write(chunk)
                n += len(chunk)
                if n > 40 * 1024 * 1024:
                    break
        print("ok", dest.name, n)
    except Exception as e:
        print("err", name, type(e).__name__)
