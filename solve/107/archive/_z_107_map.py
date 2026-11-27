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
n = int(re.search(r"n:\s*(\d+)", txt).group(1))
e = int(re.search(r"e:\s*(\d+)", txt).group(1))
print("n bits", n.bit_length(), flush=True)


def ask(payload):
    s.sendall(payload + b"\n")
    time.sleep(0.5)
    out = b""
    t0 = time.time()
    while time.time() - t0 < 5:
        try:
            d = s.recv(65536)
        except socket.timeout:
            break
        if not d:
            break
        out += d
    m = re.findall(rb"(\d{50,})", out)
    return int(m[-1]) if m else None


C = ask(b"4")
print("C bits", C.bit_length(), flush=True)
hit = None
for p in range(0, 0x20000):
    if pow(p, e, n) == C:
        hit = p
        break
print("plaintext for '4':", hit, hex(hit) if hit else None)
s.close()
