import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/346/instance/?source=library")
desc = ""
for _ in range(12):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/346/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    m = re.search(r"nc`?\s*`?([A-Za-z0-9.\-]+)\s+(\d{2,5})", desc)
    if m:
        host, port = m.group(1), int(m.group(2))
        break
print("cible:", host, port)
for attempt in range(3):
    try:
        s = socket.create_connection((host, port), timeout=15)
        s.settimeout(8)
        time.sleep(1.2)
        try:
            s.recv(65536)
        except Exception:
            pass
        s.sendall(("s" * 25 + "d" * 85).encode() + b"\n")
        time.sleep(2.0)
        out = b""
        t0 = time.time()
        while time.time() - t0 < 8:
            try:
                c = s.recv(65536)
                if not c:
                    break
                out += c
            except socket.timeout:
                break
        s.close()
        txt = out.decode("latin-1", "replace")
        print("sortie (fin):", txt[-250:].replace("\n", " | "))
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        if m:
            print("FLAG:", m.group(0))
            break
    except Exception as e:
        print("essai", attempt + 1, "ERR", type(e).__name__)
        time.sleep(2)
