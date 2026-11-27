import socket, sys, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"./_z_107url.txt").read().split()
port = int(port)
s = socket.create_connection((host, port), timeout=30)
s.settimeout(10)
buf = b""
t0 = time.time()
while time.time() - t0 < 8:
    try:
        d = s.recv(65536)
    except socket.timeout:
        break
    if not d:
        break
    buf += d
    if b"give me: " in buf:
        break
print("banner ok", flush=True)
buf = b""
i = 0
try:
    while i < 400:
        s.sendall(b"a\n")
        i += 1
        while True:
            m = re.search(rb"Here you go: (\d+)\n", buf)
            if m:
                buf = buf[m.end():]
                break
            d = s.recv(65536)
            if not d:
                raise EOFError("closed")
            buf += d
        if i % 50 == 0:
            print("  %d requetes ok, %.1fs" % (i, time.time() - t0), flush=True)
except Exception as ex:
    print("ARRET a %d requetes : %r (%.1fs)" % (i, ex, time.time() - t0), flush=True)
s.close()
