import socket, time, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.set_int_max_str_digits(0)

s = socket.create_connection(("chatelaine.cylabacademy.net", 24284), timeout=20)
s.settimeout(4)
time.sleep(0.8)
buf = b""
t0 = time.time()
while time.time() - t0 < 10:
    try:
        d = s.recv(65536)
    except socket.timeout:
        if b"give me" in buf:
            break
        continue
    if not d:
        break
    buf += d
    if b"give me" in buf:
        break
txt = buf.decode(errors="replace")
F = int(re.search(r"flag:\s*(\d+)", txt).group(1))
n = int(re.search(r"n:\s*(\d+)", txt).group(1))
Fs = str(F)
print("F digits", len(Fs), "n", len(str(n)), flush=True)


def ask(payload):
    s.sendall(payload + b"\n")
    time.sleep(0.22)
    out = b""
    t0 = time.time()
    while time.time() - t0 < 4:
        try:
            d = s.recv(65536)
        except socket.timeout:
            break
        if not d:
            break
        out += d
        if b"give me" in out:
            break
    m = re.findall(rb"(\d{50,})", out)
    return int(m[-1]) if m else None


table = {}
for c in range(32, 127):
    ct = ask(bytes([c]))
    if ct:
        table[ct] = chr(c)
print("table", len(table), flush=True)

for W in (308, 309, 307):
    best = (0, None, None)
    for pad in range(0, W):
        s2 = "0" * pad + Fs
        if len(s2) % W:
            continue
        chunks = [int(s2[i:i + W]) for i in range(0, len(s2), W)]
        if not chunks:
            continue
        n_ok = sum(1 for c in chunks if c in table)
        if n_ok > best[0]:
            best = (n_ok, pad, "".join(table.get(c, "?") for c in chunks))
    print("W=%d best matches=%d pad=%s -> %r" % (W, best[0], best[1], best[2]), flush=True)
s.close()
