import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 17503
s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(8)
time.sleep(0.6)


def read(t=1.5):
    s.settimeout(t)
    buf = b""
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            c = s.recv(16384)
            if not c:
                break
            buf += c
            if b"like to do?" in buf or b"cheese" in buf.lower()[-200:]:
                break
        except socket.timeout:
            break
    return buf.decode("utf-8", "replace")


print(read()[:300])


def enc(word):
    s.sendall(b"e\n")
    time.sleep(0.3)
    r1 = read(1.2)
    s.sendall((word + "\n").encode())
    time.sleep(0.3)
    r2 = read(1.5)
    return r1 + " || " + r2


for w in ("aaaaaaaaaa", "bbbbbbbbbb", "abcdefghij"):
    out = enc(w)
    print(f"\n--- {w} ---")
    print(out[:400])
s.close()
