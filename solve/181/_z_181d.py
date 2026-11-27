import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab


def probe(answer):
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
    if not host:
        return "pas d'instance"
    try:
        s = socket.create_connection((host, port), timeout=10)
        s.settimeout(2)
        time.sleep(0.3)
        got = b""
        for _ in range(12):
            try:
                c = s.recv(200)
                if not c:
                    break
                got += c
                break
            except socket.timeout:
                break
        # repondre 1 puis 2 (corrects) puis le troisieme avec la reponse testee
        seq = ["1", "2", answer]
        res = []
        for a in seq:
            s.sendall(a.encode() + b"\n")
            time.sleep(0.35)
            r = b""
            t0 = time.time()
            while time.time() - t0 < 1.2:
                try:
                    c = s.recv(200)
                    if not c:
                        break
                    r += c
                    break
                except socket.timeout:
                    break
            res.append(r.decode("latin-1", "replace").strip()[:20])
        s.close()
        return " | ".join(res)
    except Exception as e:
        return "ERR " + type(e).__name__


for a in ("Fizz", "fizz", "3", "FIZZ"):
    print("%-8s -> %s" % (a, probe(a)))
