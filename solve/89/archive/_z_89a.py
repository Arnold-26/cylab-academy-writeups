import sys, json, re, requests, pathlib, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.6)
cy.login()
B = pathlib.Path(r"/tmp/cylab_eps")
for cid in (89, 90):
    st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    print(f"\n=== {cid} === status={d.get('status')}")
    desc = d.get("description") or ""
    print(desc[:300])
    if d.get("status") != "RUNNING":
        cy.req("PUT", f"/api/challenges/{cid}/instance/?source=library")
        time.sleep(5)
        st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
        d = json.loads(b) if b.startswith("{") else {}
        desc = d.get("description") or ""
        print("apres PUT:", d.get("status"))
        print(desc[:400])
    urls = [u for u in re.findall(r"https?://[^\s'\"<>]+", desc) if "challenge-files" in u]
    for u in urls[:2]:
        name = u.rsplit("/", 1)[-1]
        dest = B / f"{cid}_{name}"
        if not (dest.exists() and dest.stat().st_size > 300):
            r = requests.get(u, timeout=90, verify=False)
            dest.write_bytes(r.content)
            print("  ok", name, len(r.content))
        else:
            print("  deja", name, dest.stat().st_size)
    print("  nc:", re.findall(r"nc\s+[A-Za-z0-9.\-]+\s+\d+", desc))
