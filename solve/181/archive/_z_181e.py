import sys, re, json, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
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
buf = b""
for i in range(60):
    try:
        c = s.recv(4096)
        if not c:
            break
        buf += c
    except socket.timeout:
        if buf:
            break
txt = buf.decode("latin-1", "replace")
if not txt:
    print("pas de banner")
else:
    s.sendall(b"fizzbuzz\n")
    time.sleep(0.4)
    out = b""
    t0 = time.time()
    while time.time() - t0 < 3:
        try:
            c = s.recv(4096)
            if not c:
                break
            out += c
        except socket.timeout:
            break
    t2 = out.decode("latin-1", "replace")
    print("apres fizzbuzz:", repr(t2[:200]))
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", t2)
    if m:
        print("FLAG:", m.group(0))
    else:
        # continuer : peut-etre plusieurs questions
        for k in range(6):
            s.sendall(b"fizzbuzz\n")
            time.sleep(0.3)
            r = b""
            t0 = time.time()
            while time.time() - t0 < 1.5:
                try:
                    c = s.recv(4096)
                    if not c:
                        break
                    r += c
                except socket.timeout:
                    break
            tt = r.decode("latin-1", "replace")
            print("  [%d] %r" % (k, tt[:120]))
            m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", tt)
            if m:
                print("FLAG:", m.group(0))
                break
s.close()
