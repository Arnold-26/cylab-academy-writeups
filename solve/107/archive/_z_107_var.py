import socket, time, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.set_int_max_str_digits(0)

txt = open(r"./_z_107_banner.txt", encoding="utf-8").read()
n = int(re.search(r"n:\s*(\d+)", txt).group(1))
e = int(re.search(r"e:\s*(\d+)", txt).group(1))
F = int(re.search(r"flag:\s*(\d+)", txt).group(1))

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
print("C4:", C4.bit_length(), "C1:", C1.bit_length(), "C41:", C41.bit_length())
print("var-len join (C4<<len(C1))|C1 == C41:", (C4 << C1.bit_length()) | C1 == C41)
print("pow(52)^e==C4:", pow(0x34, e, n) == C4, " pow(49)^e==C1:", pow(0x31, e, n) == C1)
s.close()

# now split F using variable-length concatenation
total = F.bit_length()
pos = total
out = ""
cands = [(chr(c), pow(c, e, n)) for c in range(32, 127)]
while pos > 0:
    hit = None
    for ch, ct in cands:
        L = ct.bit_length()
        if L <= pos and ((F >> (pos - L)) & ((1 << L) - 1)) == ct:
            hit = (ch, L)
            break
    if not hit:
        print("stuck at pos", pos, "of", total)
        break
    out += hit[0]
    pos -= hit[1]
print("decoded:", out)
