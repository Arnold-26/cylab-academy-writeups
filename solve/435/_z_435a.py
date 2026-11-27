import sys, json, re, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.7)
cy.login()
B = pathlib.Path(r"/tmp/cylab_eps")
for cid in (435, 440):
    st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    print(f"=== {cid} ===")
    for u in re.findall(r"https?://[^\s'\"<>]+", desc):
        if "challenge-files" not in u:
            continue
        name = u.rsplit("/", 1)[-1]
        dest = B / f"{cid}_{name}"
        if not (dest.exists() and dest.stat().st_size > 100):
            try:
                r = requests.get(u, timeout=60, verify=False)
                dest.write_bytes(r.content)
            except Exception as e:
                print("  err", name, type(e).__name__)
                continue
        print("  ", dest.name, dest.stat().st_size)
