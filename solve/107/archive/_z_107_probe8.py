import socket, sys, time, re, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"./_z_107url.txt").read().split()
port = int(port)
s = socket.create_connection((host, port), timeout=30)
s.settimeout(5)

def readbanner():
    buf = b""
    end = time.time() + 6
    while time.time() < end:
        try:
            d = s.recv(65536)
        except socket.timeout:
            break
        if not d:
            break
        buf += d
        if b"give me: " in buf:
            break
    return buf

bt = readbanner()
print("banner len:", len(bt), "fin:", bt[-60:])
s.sendall(b"a\n")
resp = b""
end = time.time() + 5
while time.time() < end:
    try:
        d = s.recv(65536)
    except socket.timeout:
        break
    if not d:
        break
    resp += d
    if b"\n" in resp:
        break
print("resp len:", len(resp))
print("resp repr debut:", resp[:60])
print("resp repr fin:", resp[-80:])
s.close()
