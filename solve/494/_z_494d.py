import sys, re, json, time, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
urllib3.disable_warnings()

cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/494/instance/?source=library")
base = None
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/494/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"(https?://[A-Za-z0-9.\-]+:\d+)", d.get("description") or "")
    if m:
        base = m.group(1).rstrip("/") + "/"
        break
print("base:", base)
tests = [
    ("une porte bidon", [{"input1": 1, "input2": 1, "output": 1}]),
    ("quatre portes bidon", [{"input1": i, "input2": i, "output": i + 10} for i in range(1, 5)]),
    ("vide", []),
]
for label, circ in tests:
    try:
        r = requests.post(base + "check", json={"circuit": circ}, timeout=30)
        print("%-24s -> %d %s" % (label, r.status_code, r.text[:200]))
    except Exception as e:
        print(label, "ERR", type(e).__name__)
