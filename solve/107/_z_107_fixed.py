import socket, time, re, sys, math
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
e = int(re.search(r"e:\s*(\d+)", txt).group(1))
W = n.bit_length()
print("F bits", F.bit_length(), "W", W, "ratio", F.bit_length() / W, flush=True)


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
        table[chr(c)] = ct
print("table", len(table), flush=True)

K = math.ceil(F.bit_length() / W)
print("chunks hypothesis K =", K, flush=True)
for k in (K, K + 1, K - 1):
    if k <= 0:
        continue
    total = k * W
    if total < F.bit_length():
        continue
    padded = F << (total - F.bit_length())
    out = []
    ok = True
    for i in range(k):
        chunk = (padded >> (W * (k - 1 - i))) & ((1 << W) - 1)
        hit = None
        for ch, ct in table.items():
            if ct == chunk:
                hit = ch
                break
        if hit is None:
            ok = False
            out.append("?")
        else:
            out.append(hit)
    print("K=%d -> %s %s" % (k, "".join(out), "FULL MATCH" if ok else ""), flush=True)
s.close()
