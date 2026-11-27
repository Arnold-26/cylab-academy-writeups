import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.4)
cy.login()
for cid in (346, 446):
    cy.req("PUT", f"/api/challenges/{cid}/instance/?source=library")
    host = port = None
    desc = ""
    for _ in range(10):
        time.sleep(0.8)
        st, b = cy.req("GET", f"/api/challenges/{cid}/instance/")
        d = json.loads(b) if b.startswith("{") else {}
        desc = d.get("description") or ""
        m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", desc)
        if m:
            host, port = m.group(2), int(m.group(3))
            break
    print("%d cible: %s %s" % (cid, host, port))
    if not host:
        print("   desc:", desc[:150])
        continue
    try:
        s = socket.create_connection((host, port), timeout=15)
        s.settimeout(6)
        time.sleep(1.0)
        try:
            s.recv(65536)
        except Exception:
            pass
        moves = ("s" * 25 + "d" * 85) if cid == 346 else ("s" * 25 + "d" * 85)
        s.sendall(moves.encode() + b"\n")
        time.sleep(1.5)
        out = b""
        t0 = time.time()
        while time.time() - t0 < 6:
            try:
                c = s.recv(65536)
                if not c:
                    break
                out += c
            except socket.timeout:
                break
        s.close()
        txt = out.decode("latin-1", "replace")
        tail = txt[-300:].replace("\n", " | ")
        print("   sortie:", tail[:250])
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        if m:
            print("   FLAG:", m.group(0))
    except Exception as e:
        print("   ERR", type(e).__name__)
