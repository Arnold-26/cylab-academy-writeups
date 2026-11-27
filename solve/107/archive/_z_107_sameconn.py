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
e = int(re.search(r"e:\s*(\d+)", txt).group(1))
print("flag bits", F.bit_length(), "n bits", n.bit_length(), "e", e)


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


C4a = ask(b"4")
C4b = ask(b"4")
C1 = ask(b"1")
C41 = ask(b"41")
print("C4a==C4b (deterministic):", C4a == C4b)
for name, v in (("int 4", 4), ("b'4'", 0x34), ("str->int('4')", 4)):
    print(name, pow(v, e, n) == C4a)
print("C41 bits", C41.bit_length(), "C4 bits", C4a.bit_length(), "C1 bits", C1.bit_length())
print("join var:", (C4a << C1.bit_length()) | C1 == C41)
print("join 1024:", (C4a << 1024) | C1 == C41)
s.close()
open(r"./_z_107_same.txt", "w", encoding="utf-8").write("%d\n%d\n%d\n" % (F, n, e))
