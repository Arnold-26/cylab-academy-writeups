import sys, json, re, time, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.8)
cy.login()
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
cy.req("PUT", "/api/challenges/133/instance/?source=library")
desc = ""
for _ in range(15):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/133/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        if "challenge-files" in desc:
            break
print(desc[:700])
urls = re.findall(r"https?://[^\s'\"<>]+", desc)
print("\n%d urls" % len(urls))
for u in urls:
    name = u.rsplit("/", 1)[-1]
    dest = B / f"133_{name}"
    if dest.exists() and dest.stat().st_size > 100:
        print("deja", dest.name, dest.stat().st_size)
        continue
    try:
        r = requests.get(u, timeout=90, verify=False)
        dest.write_bytes(r.content)
        print("ok", dest.name, len(r.content))
    except Exception as e:
        print("err", name, type(e).__name__)
