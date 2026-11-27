import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/345/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/345/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)
seq = "w" * 4 + "a" * 8 + "s" * 29 + "d" * 93
s = socket.create_connection((host, port), timeout=25)
s.settimeout(10)
time.sleep(0.6)
try:
    s.recv(65536)
except Exception:
    pass
s.sendall((seq + "\n").encode())
tail = b""
pos = []
t0 = time.time()
while time.time() - t0 < 60:
    try:
        c = s.recv(65536)
    except socket.timeout:
        break
    if not c:
        break
    tail = (tail + c)[-3000:]
    for m in re.finditer(rb"Player position: (-?\d+) (-?\d+)", c):
        pos.append((int(m.group(1)), int(m.group(2))))
    for m in re.finditer(rb"Player has flag: (\d+)", c):
        pos.append(("flag", int(m.group(1))))
s.close()
print("dernieres positions:", pos[-6:])
print("=== fin ===")
print(tail.decode("utf-8", "replace")[-600:])
