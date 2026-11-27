import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.3)
cy.login()
cy.req("PUT", "/api/challenges/181/instance/?source=library")
host = port = None
for _ in range(10):
    time.sleep(0.7)
    st, b = cy.req("GET", "/api/challenges/181/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(2), int(m.group(3))
        break
print("cible:", host, port)
s = socket.create_connection((host, port), timeout=12)
s.settimeout(2)
time.sleep(0.3)


def pump(t=1.5):
    out = b""
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            c = s.recv(4096)
            if not c:
                break
            out += c
        except socket.timeout:
            break
    return out.decode("latin-1", "replace")


print("banner:", repr(pump(1.0)))
for ans in (b"1\x00\n", b"2\x00\n", b"fizz\x00\n", b"4\x00\n", b"buzz\x00\n"):
    s.sendall(ans)
    r = pump(1.0)
    print("%-12r -> %r" % (ans, r[:40]))
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r)
    if m:
        print("FLAG:", m.group(0))
        break
s.close()
