import sys, json, re, time, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.7)
cy.login()
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
for cid in (352, 146, 187):
    cy.req("PUT", f"/api/challenges/{cid}/instance/?source=library")
    time.sleep(4)
    st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    print(f"\n=== {cid} [{d.get('status')}] ===")
    print(desc[:450])
    for u in re.findall(r"https?://[^\s'\"<>]+", desc):
        if "challenge-files" in u:
            name = u.rsplit("/", 1)[-1]
            dest = B / f"{cid}_{name}"
            if not (dest.exists() and dest.stat().st_size > 100):
                try:
                    r = requests.get(u, timeout=60, verify=False)
                    dest.write_bytes(r.content)
                    print("   ok", dest.name, dest.stat().st_size)
                except Exception as e:
                    print("   err", name, type(e).__name__)
            else:
                print("   deja", dest.name, dest.stat().st_size)
