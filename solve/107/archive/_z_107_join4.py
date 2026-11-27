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


def ask(payload):
    s.sendall(payload + b"\n")
    time.sleep(0.3)
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


A = ask(b"4")
B = ask(b"1")
AB = ask(b"41")
print("A*B==AB:", A * B == AB)
print("A+B==AB:", A + B == AB)
print("A^B==AB:", (A ^ B) == AB)
print("A*B bits", (A * B).bit_length(), "AB bits", AB.bit_length())
print("AB/(A*B) ~", AB // (A * B) if A * B else None)
# maybe AB == A*B mod n^2 or mod something
for m in (n, n * n, 1 << 2048):
    print("A*B mod m == AB:", (A * B) % m == AB)
s.close()
