import sys, json, re, time, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=1.2)
cy.login()
cy.req("PUT", "/api/challenges/131/instance/?source=library")
url = None
for _ in range(15):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/131/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        cands = [c for c in re.findall(r"https?://[A-Za-z0-9.\-]+\.cylabacademy\.net(?::\d+)?", desc) if "challenge-files" not in c]
        if cands:
            url = cands[0]
        break
print("131:", url)
OUT = pathlib.Path(r"/tmp/cylab_wasm")
OUT.mkdir(exist_ok=True)
if url:
    base = url.rstrip("/")
    r = requests.get(base + "/aD8SvhyVkb", timeout=30, verify=False)
    w = OUT / "aD8SvhyVkb.wasm"
    w.write_bytes(r.content)
    print("wasm:", len(r.content), w)
    # strings dans le wasm
    strs = re.findall(rb"[ -~]{4,}", r.content)
    for s in strs[-40:]:
        print(s[:120])
