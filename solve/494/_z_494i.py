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

# d'abord verifier que le circuit gagnant marche encore, puis tester des variantes "flag"
tests = {
    "gagnant": [{"input1": i, "input2": i, "output": i - 4} for i in range(5, 9)],
    "noeuds eleves": [{"input1": i, "input2": i, "output": i} for i in range(1, 5)],
    "auto-nand 1..4": [{"input1": i, "input2": i, "output": i} for i in range(1, 9)],
    "grand circuit": [{"input1": i, "input2": i, "output": (i % 8) + 1} for i in range(1, 33)],
    "sortie 0x1337": [{"input1": i, "input2": i, "output": 0x1337} for i in range(1, 5)],
}
for label, circ in tests.items():
    try:
        r = requests.post(base + "check", json={"circuit": circ}, timeout=40)
        print("%-18s -> %d %s" % (label, r.status_code, r.text[:170]))
    except Exception as e:
        print(label, "ERR", type(e).__name__)
