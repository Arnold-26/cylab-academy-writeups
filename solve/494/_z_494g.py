import sys, re, json, time, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
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
tests = {
    "4 NOT : out=5..8": [{"input1": i, "input2": i, "output": i + 4} for i in range(1, 5)],
    "4 NOT : out=1..4 in=5..8": [{"input1": i, "input2": i, "output": i - 4} for i in range(5, 9)],
    "1 porte (1,2)->3": [{"input1": 1, "input2": 2, "output": 3}],
    "8 NOT (bits)": [{"input1": i, "input2": i, "output": i + 8} for i in range(1, 9)],
}
for label, circ in tests.items():
    try:
        r = requests.post(base + "check", json={"circuit": circ}, timeout=40)
        print("%-26s -> %d %s" % (label, r.status_code, r.text[:180]))
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
        if m:
            print("   FLAG:", m.group(0))
            break
    except Exception as e:
        print(label, "ERR", type(e).__name__)
