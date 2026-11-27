import sys, re, socket, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = "mars.cylabacademy.net", 31929


def talk(lines, wait=4.0):
    s = socket.create_connection((host, port), timeout=15)
    s.settimeout(6)
    time.sleep(0.8)
    out = b""
    try:
        out += s.recv(65536)
    except Exception:
        pass
    for ln in lines:
        s.sendall((ln + "\n").encode())
        time.sleep(0.35)
        try:
            out += s.recv(65536)
        except Exception:
            pass
    s.sendall(b"\n")
    time.sleep(0.4)
    t0 = time.time()
    while time.time() - t0 < wait:
        try:
            c = s.recv(65536)
            if not c:
                break
            out += c
        except socket.timeout:
            break
    s.close()
    return out.decode("latin-1", "replace")


for lines in (["1", "2", "3", "3"], ["%p", "%p", "%p", "%p"], ["1", "2", "3", "2"]):
    o = talk(lines)
    print("=== %r ===" % lines)
    print("  ", o[:500].replace("\n", " | "))
