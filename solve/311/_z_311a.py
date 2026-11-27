import sys, json, re, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
cy = CyLab(delay=0.7)
cy.login()
st, b = cy.req("GET", "/api/challenges/116/")
d = json.loads(b) if b.startswith("{") else {}
print("116:", d.get("name"), "| retired:", d.get("retired"), "| maintenance:", d.get("under_maintenance"),
      "| event:", (d.get("event") or {}).get("name"))
print()
for cid in (311, 494):
    cy.req("PUT", f"/api/challenges/{cid}/instance/?source=library")
    time.sleep(5)
    st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    print(f"=== {cid} {d.get('status')} ===")
    print(desc[:350])
    urls = [u for u in re.findall(r"https?://[^\s'\"<>]+", desc) if "challenge-files" in u]
    for u in urls[:1]:
        name = u.rsplit("/", 1)[-1]
        dest = B / f"{cid}_{name}"
        print("  fichier attendu:", name)
    print()
for f in sorted(B.glob("311_*")) + sorted(B.glob("494_*")):
    print("present:", f.name, f.stat().st_size)
