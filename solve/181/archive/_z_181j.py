import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = "chatelaine.cylabacademy.net", 15649


def session(answers):
    s = socket.create_connection((host, port), timeout=15)
    s.settimeout(3)
    buf = b""
    log = []
    for a in answers:
        t0 = time.time()
        while time.time() - t0 < 3:
            m = re.search(rb"(\d+)\?", buf)
            if m:
                break
            try:
                c = s.recv(4096)
                if not c:
                    break
                buf += c
            except socket.timeout:
                break
        s.sendall(a.encode() + b"\n")
        time.sleep(0.15)
    time.sleep(0.6)
    out = b""
    t0 = time.time()
    while time.time() - t0 < 3:
        try:
            c = s.recv(8192)
            if not c:
                break
            out += c
        except socket.timeout:
            break
    s.close()
    return buf + out


print("=== reponse fausse immediate ===")
print(session(["x"]).decode("latin-1", "replace")[-400:])
print("\n=== 3 bonnes puis fausse ===")
print(session(["1", "2", "fizz", "x"]).decode("latin-1", "replace")[-400:])
print("\n=== 6 bonnes puis fausse ===")
print(session(["1", "2", "fizz", "1", "2", "fizz", "x"]).decode("latin-1", "replace")[-500:])
