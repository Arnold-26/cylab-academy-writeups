import sys, json, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=1.2)
cy.login()
for cid in (206, 456):
    try:
        cy.req("PUT", f"/api/challenges/{cid}/instance/?source=library")
    except Exception:
        pass
    time.sleep(0.3)
for cid in (206, 456):
    got = False
    for _ in range(12):
        time.sleep(2)
        st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
        d = json.loads(b) if b.startswith("{") else {}
        if d.get("status") == "RUNNING":
            desc = d.get("description") or ""
            urls = [u for u in re.findall(r"https?://[^\s'\"<>]+", desc) if "challenge-files" in u]
            print(f"\n=== {cid} ===")
            print("DESC:", desc[:600].replace("\n", " "))
            print("fichiers:", [u.rsplit('/',1)[-1] for u in urls][:3])
            for u in urls:
                name = u.rsplit("/", 1)[-1]
                dest = r"/tmp/cylab_bin" + "\\" + f"{cid}_{name}"
                import pathlib, requests
                requests.packages.urllib3.disable_warnings()
                p = pathlib.Path(dest)
                if not (p.exists() and p.stat().st_size > 0):
                    r = requests.get(u, timeout=90, verify=False)
                    p.write_bytes(r.content)
                    print("ok:", name, len(r.content))
            got = True
            break
    if not got:
        print(f"\n=== {cid} : pas demarre ===")
