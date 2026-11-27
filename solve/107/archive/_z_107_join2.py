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
W = n.bit_length()
print("W", W, flush=True)


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
print("bits", A.bit_length(), B.bit_length(), AB.bit_length())
tests = {
    "A*n+B": A * n + B,
    "A<<len(B)|B": (A << B.bit_length()) | B,
    "A<<len(A)|B": (A << A.bit_length()) | B,
    "A<<W|B": (A << W) | B,
    "A<<1024|B": (A << 1024) | B,
    "A*10^309+B": A * 10 ** 309 + B,
    "B<<len(A)|A (reversed)": (B << A.bit_length()) | A,
    "A*2^1030+B": A * (1 << 1030) + B,
}
for k, v in tests.items():
    print(k, v == AB)
# also try to locate A and B bit patterns inside AB
ab = bin(AB)[2:]
a = bin(A)[2:]
b = bin(B)[2:]
print("A prefix of AB:", ab.startswith(a))
print("B suffix of AB:", ab.endswith(b))
print("AB len", len(ab), "A len", len(a), "B len", len(b))
print("gap:", len(ab) - len(a) - len(b))
s.close()
