import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/171/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/171/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    m = re.search(r"`?\s*([A-Za-z0-9.\-]+\.cylabacademy\.net):(\d{2,5})", desc)
    if m:
        host, port = m.group(1), int(m.group(2))
        break
print("cible:", host, port)
pw = "reverseengineericanbarelyforward"
for attempt in range(4):
    try:
        s = socket.create_connection((host, port), timeout=12)
        s.settimeout(6)
        time.sleep(0.4)
        try:
            banner = s.recv(500)
            print("banner:", banner[:120])
        except Exception:
            pass
        s.sendall(pw.encode() + b"\n")
        time.sleep(0.8)
        out = b""
        t0 = time.time()
        while time.time() - t0 < 6:
            try:
                c = s.recv(4096)
                if not c:
                    break
                out += c
            except socket.timeout:
                break
        s.close()
        txt = out.decode("latin-1", "replace")
        print("reponse:", txt.replace("\n", " ")[:300])
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        if m:
            print("FLAG:", m.group(0))
            break
    except Exception as e:
        print("essai", attempt + 1, "ERR", type(e).__name__)
        time.sleep(2)
