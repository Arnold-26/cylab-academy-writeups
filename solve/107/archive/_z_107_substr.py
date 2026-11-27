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
Fbits = bin(F)[2:]
print("F bits", len(Fbits), flush=True)


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


found = {}
for c in range(32, 127):
    ct = ask(bytes([c]))
    if not ct:
        continue
    b = bin(ct)[2:]
    idx = Fbits.find(b)
    if idx >= 0:
        found[chr(c)] = (idx, len(b))
print("substring hits:", found, flush=True)
s.close()
