import socket, time, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.set_int_max_str_digits(0)

txt = open(r"./_z_107_banner.txt", encoding="utf-8").read()
n = int(re.search(r"n:\s*(\d+)", txt).group(1))
e = int(re.search(r"e:\s*(\d+)", txt).group(1))

s = socket.create_connection(("chatelaine.cylabacademy.net", 24284), timeout=20)
s.settimeout(4)
time.sleep(0.6)
buf = b""
t0 = time.time()
while time.time() - t0 < 8:
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


C4 = ask(b"4")
C1 = ask(b"1")
C41 = ask(b"41")
print("bits", C4.bit_length(), C1.bit_length(), C41.bit_length())
print("C4*2^1024+C1   == C41:", C4 * (1 << 1024) + C1 == C41)
print("C4*n+C1        == C41:", C4 * n + C1 == C41)
print("C4*2^2048+C1   == C41:", C4 * (1 << 2048) + C1 == C41)
B = 1 << (n.bit_length())
print("B=2^1024 :", B)
# try fixed decimal width
w = len(str(n))
print("dec width", w, int(str(C4) + str(C1).zfill(w)) == C41)
s.close()
