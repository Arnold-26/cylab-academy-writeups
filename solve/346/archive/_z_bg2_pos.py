import socket, time, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HOST, PORT = "xebec.cylabacademy.net", 27860
keys = b"l]" + b"w" * 4 + b"d" * 47 + b"w"
line = keys + b"\n"
s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(1.0)
time.sleep(0.5)
t0 = time.time(); last = time.time(); buf = b""
while time.time() - t0 < 6:
    try:
        d = s.recv(65536)
    except socket.timeout:
        if time.time() - last > 0.8:
            break
        continue
    if not d:
        break
    buf += d; last = time.time()
s.sendall(line)
out = b""
t0 = time.time(); last = time.time()
while time.time() - t0 < 30:
    try:
        d = s.recv(65536)
    except socket.timeout:
        if time.time() - last > 3:
            break
        continue
    if not d:
        break
    out += d; last = time.time()
s.close()
allout = buf + out
pos = re.findall(rb"Player position: (-?\d+) (-?\d+)", allout)
print("num maps:", len(pos))
print("first:", pos[:3])
print("last:", pos[-3:])
print("flag:", re.search(rb"(academy|picoCTF)\{[^}]{1,120}\}", allout))
print("tail:", allout[-160:])
