import socket, time, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
s = socket.create_connection(("chatelaine.cylabacademy.net", 24284), timeout=20)
s.settimeout(4)
time.sleep(0.6)
buf = b""
t0 = time.time()
while time.time() - t0 < 5:
    try:
        d = s.recv(65536)
    except socket.timeout:
        break
    if not d:
        break
    buf += d
print("BANNER tail:", buf[-400:])
s.sendall(b"41\n")
time.sleep(1.0)
out = b""
t0 = time.time()
while time.time() - t0 < 5:
    try:
        d = s.recv(65536)
    except socket.timeout:
        break
    if not d:
        break
    out += d
print("RESP:", out[:600])
s.close()
