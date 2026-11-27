import sys, json, re, time, pathlib, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=1.2)
cy.login()
BASE = pathlib.Path(r"/tmp/cylab_cr")
BASE.mkdir(exist_ok=True)
for cid in (148, 297):
    st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    urls = [u for u in re.findall(r"https?://[^\s'\"<>]+", desc) if "challenge-files" in u]
    print(f"\n=== {cid} ===")
    for u in urls:
        dest = BASE / u.rsplit("/", 1)[-1]
        r = requests.get(u, timeout=120, verify=False)
        dest.write_bytes(r.content)
        print("fichier:", dest.name, dest.stat().st_size)
        if dest.suffix == ".py":
            print(dest.read_text(encoding="utf-8", errors="replace")[:1500])
