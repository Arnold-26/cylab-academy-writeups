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
print("flag bits", F.bit_length(), "n", n.bit_length(), flush=True)


def ask(payload):
    s.sendall(payload + b"\n")
    time.sleep(0.25)
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
    if ct is None:
        print("no ct for", chr(c), flush=True)
        continue
    table[chr(c)] = ct
print("collected", len(table), flush=True)

items = sorted(table.items(), key=lambda kv: kv[1].bit_length(), reverse=True)
pos = F.bit_length()
out = ""
while pos > 0:
    hit = None
    for ch, ct in items:
        L = ct.bit_length()
        if L <= pos and ((F >> (pos - L)) & ((1 << L) - 1)) == ct:
            hit = (ch, L)
            break
    if not hit:
        print("stuck at pos", pos, "of", F.bit_length())
        break
    out += hit[0]
    pos -= hit[1]
print("DECODED:", out)
if "academy{" in out or "picoCTF{" in out:
    open(r"./_z_107_flag.txt", "w").write(out)
s.close()
