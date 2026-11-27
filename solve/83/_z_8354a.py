import sys, re, json, time, requests, urllib3, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
urllib3.disable_warnings()
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
cy = CyLab(delay=0.4)
cy.login()
for cid in (83, 54):
    cy.req("PUT", f"/api/challenges/{cid}/instance/?source=library")
    desc = ""
    for _ in range(8):
        time.sleep(0.8)
        st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
        d = json.loads(b) if b.startswith("{") else {}
        desc = d.get("description") or ""
        if "challenge-files" in desc:
            break
    print("=== %d ===" % cid)
    print(desc[:400].replace("\n", " "))
    for u in re.findall(r"https?://[^\s'\"<>]+", desc):
        if "challenge-files" not in u:
            continue
        name = u.rsplit("/", 1)[-1]
        dest = B / f"{cid}_{name}"
        try:
            r = requests.get(u, timeout=90, verify=False)
            dest.write_bytes(r.content)
            print("   ok", dest.name, len(r.content))
        except Exception as e:
            print("   err", name, type(e).__name__)
    print()
