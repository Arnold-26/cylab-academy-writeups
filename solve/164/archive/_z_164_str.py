import socket, sys, time

HOST, PORT = sys.argv[1], int(sys.argv[2])
idxs = [int(x) for x in sys.argv[3].split(",")]

fmt = "|".join("%%%d$s" % i for i in idxs).encode()
s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(4)
time.sleep(0.3)
s.recv(4096)
s.sendall(b"1\n")
time.sleep(0.4)
try:
    s.recv(4096)
except Exception:
    pass
s.sendall(fmt + b"\n")
time.sleep(0.6)
out = b""
try:
    while True:
        d = s.recv(8192)
        if not d:
            break
        out += d
except Exception:
    pass
s.close()
txt = out.decode(errors="replace")
seg = txt.split("Buying stonks with token:")[-1]
print(seg[:3000])
