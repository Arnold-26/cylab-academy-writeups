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
    m = re.search(r"([A-Za-z0-9.\-]+\.cylabacademy\.net)[:\s]+(\d{2,5})", desc)
    if m:
        host, port = m.group(1), int(m.group(2))
        break
print("cible:", host, port)
flag = None
for attempt in range(4):
    try:
        s = socket.create_connection((host, port), timeout=12)
        s.settimeout(6)
        time.sleep(0.5)
        try:
            print("banner:", s.recv(300)[:80])
        except Exception:
            pass
        s.sendall(b"reverseengineericanbarelyforward\n")
        time.sleep(0.7)
        out = b""
        t0 = time.time()
        while time.time() - t0 < 3:
            try:
                c = s.recv(4096)
                if not c:
                    break
                out += c
                if b"unhashed" in out:
                    break
            except socket.timeout:
                break
        print("etape1:", out.decode("latin-1", "replace")[-120:].replace("\n", " "))
        s.sendall(b"goldfish\n")
        time.sleep(1.0)
        out2 = b""
        t0 = time.time()
        while time.time() - t0 < 6:
            try:
                c = s.recv(4096)
                if not c:
                    break
                out2 += c
            except socket.timeout:
                break
        s.close()
        txt = out2.decode("latin-1", "replace")
        print("etape2:", txt.replace("\n", " ")[:300])
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        if m:
            flag = m.group(0)
            print("FLAG:", flag)
            break
    except Exception as e:
        print("essai", attempt + 1, "ERR", type(e).__name__)
        time.sleep(2)
