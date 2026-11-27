import sys, re, json, time, requests, urllib3, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/153/instance/?source=library")
base = None
for _ in range(12):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/153/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"(http://[A-Za-z0-9.\-]+:\d+/)", d.get("description") or "")
    if m:
        base = m.group(1)
        break
print("base:", base)
for k in range(10):
    try:
        rr = requests.get(base + "qCCYI0ajpD", timeout=30)
        dest = B / "153_qCCYI0ajpD.wasm"
        dest.write_bytes(rr.content)
        print("wasm:", len(rr.content), "magic:", rr.content[:4])
        break
    except Exception as e:
        time.sleep(1.5)
