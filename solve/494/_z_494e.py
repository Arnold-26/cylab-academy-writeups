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

variants = {}
# hypothese A : indices de bits = offset_octet*8 + k, entree a 0x200A (apres len+4), sortie a 0x1004
IN_A, OUT_A = 0x200A * 8, 0x1004 * 8
variants["A bits in=0x200A out=0x1004"] = [{"input1": IN_A + i, "input2": IN_A + i, "output": OUT_A + i} for i in range(64)]
# hypothese B : entree a 0x2000, sortie a 0x1000
IN_B, OUT_B = 0x2000 * 8, 0x1000 * 8
variants["B bits in=0x2000 out=0x1000"] = [{"input1": IN_B + i, "input2": IN_B + i, "output": OUT_B + i} for i in range(64)]
# hypothese C : indices d'octets (pas de *8)
variants["C octets in=0x200A out=0x1004"] = [{"input1": 0x200A + i, "input2": 0x200A + i, "output": 0x1004 + i} for i in range(64)]

for label, circ in variants.items():
    try:
        r = requests.post(base + "check", json={"circuit": circ}, timeout=40)
        print("%-32s -> %d %s" % (label, r.status_code, r.text[:160]))
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
        if m:
            print("   FLAG:", m.group(0))
            break
    except Exception as e:
        print(label, "ERR", type(e).__name__)
