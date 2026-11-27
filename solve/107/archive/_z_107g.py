import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.set_int_max_str_digits(0)
sys.path.insert(0, r".")
from cylab2 import CyLab


def get_target():
    cy = CyLab(delay=0.3)
    cy.login()
    cy.req("PUT", "/api/challenges/107/instance/?source=library")
    for _ in range(10):
        time.sleep(0.8)
        st, b = cy.req("GET", "/api/challenges/107/instance/")
        d = json.loads(b) if b.startswith("{") else {}
        m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
        if m:
            return m.group(1), int(m.group(2))
    return None, None


def session(host, port, payloads):
    s = socket.create_connection((host, port), timeout=20)
    s.settimeout(3)
    out = b""
    t0 = time.time()
    while time.time() - t0 < 3:
        try:
            c = s.recv(65536)
            if not c:
                break
            out += c
            if b"give me" in out:
                break
        except socket.timeout:
            break
    resps = []
    for p in payloads:
        s.sendall(p.encode() + b"\n")
        time.sleep(0.35)
        r = b""
        t0 = time.time()
        while time.time() - t0 < 2:
            try:
                c = s.recv(65536)
                if not c:
                    break
                r += c
            except socket.timeout:
                break
        resps.append(r.decode("latin-1", "replace"))
    s.close()
    return out.decode("latin-1", "replace"), resps


host, port = get_target()
print("cible:", host, port)
banner, resps = session(host, port, ["A", "B", "ab"])
print("banner len:", len(banner))
mnum = re.search(r"flag:\s*(\d+)", banner)
flagnum = mnum.group(1) if mnum else ""
print("flag digits:", len(flagnum))
for i, r in enumerate(resps):
    print("resp[%d]: %r" % (i, r[:160]))
