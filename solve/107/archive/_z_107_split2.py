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
print("F digits", len(Fs), "n digits", len(str(n)), flush=True)


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

for W in (308, 307, 309):
    for lead in range(0, W):
        pad = lead
        total = len(Fs) + pad
        if total % W:
            continue
        s2 = "0" * pad + Fs
        chunks = [int(s2[i:i + W]) for i in range(0, len(s2), W)]
        out = "".join(table.get(c, "?") for c in chunks)
        nmiss = out.count("?")
        if nmiss <= 2:
            print("W=%d pad=%d chunks=%d -> %r (miss %d)" % (W, pad, len(chunks), out, nmiss), flush=True)
        if nmiss == 0:
            open(r"./_z_107_flag.txt", "w").write(out)
s.close()
