import sys, re, json, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/181/instance/?source=library")
host = port = None
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/181/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(2), int(m.group(3))
        break
print("cible:", host, port)
s = socket.create_connection((host, port), timeout=12)
s.settimeout(4)
time.sleep(0.4)
out = b""
t0 = time.time()
while time.time() - t0 < 4:
    try:
        c = s.recv(4096)
        if not c:
            break
        out += c
    except socket.timeout:
        break
txt = out.decode("latin-1", "replace")
print("banner:", repr(txt[:400]))
nums = re.findall(r"\d+", txt)
print("nombres:", nums[:5])
s.close()
