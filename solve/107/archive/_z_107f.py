import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.set_int_max_str_digits(0)
sys.path.insert(0, r".")
from cyab import CyLab if False else None
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


def talk(host, port, payload, wait=2.0):
    s = socket.create_connection((host, port), timeout=20)
    s.settimeout(wait + 2)
    out = b""
    t0 = time.time()
    while time.time() - t0 < wait:
        try:
            c = s.recv(65536)
            if not c:
                break
            out += c
            if b"give me" in out:
                break
        except socket.timeout:
            break
    s.sendall(payload)
    time.sleep(0.8)
    out2 = b""
    t0 = time.time()
    while time.time() - t0 < 3:
        try:
            c = s.recv(65536)
            if not c:
                break
            out2 += c
        except socket.timeout:
            break
    s.close()
    return out, out2


host, port = get_target()
print("cible:", host, port)
banner, _ = talk(host, port, b"\n")
txt = banner.decode("latin-1", "replace")
mnum = re.search(r"flag:\s*(\d+)", txt)
flagnum = mnum.group(1)
print("flag digits:", len(flagnum))
# oracle : un caractere
_, resp = talk(host, port, b"A\n")
print("reponse oracle A:", repr(resp[:200]))
