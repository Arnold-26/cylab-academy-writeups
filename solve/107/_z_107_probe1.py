import socket, sys, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"./_z_107url.txt").read().split()
port = int(port)
s = socket.create_connection((host, port), timeout=20)
s.settimeout(5)

buf = b""
def drain(t=1.5):
    global buf
    end = time.time() + t
    while time.time() < end:
        try:
            d = s.recv(65536)
        except socket.timeout:
            break
        if not d:
            break
        buf += d
    return buf

drain(2.0)
print("=== BANNER (%d bytes) ===" % len(buf))
txt = buf.decode("latin-1")
for line in txt.split("\n"):
    print("  [%d] %s" % (len(line), line if len(line) < 200 else line[:100] + "..." + line[-60:]))
buf = b""
s.sendall(b"4\n")
drain(2.0)
print("=== enc(4) len=%d ===" % len(buf))
print("  raw:", buf[:200])
buf = b""
s.sendall(b"41\n")
drain(2.0)
print("=== enc(41) len=%d ===" % len(buf))
print("  raw:", buf[:200])
buf = b""
s.sendall(b"a\n")
drain(2.0)
print("=== enc(a) len=%d ===" % len(buf))
print("  raw:", buf[:300])
buf = b""
s.sendall(b"a\n")
drain(2.0)
print("=== enc(a) again len=%d ===" % len(buf))
print("  raw:", buf[:300])
s.close()
