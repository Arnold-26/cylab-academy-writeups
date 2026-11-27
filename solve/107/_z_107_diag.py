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
W = len(str(n))
print("F digits", len(Fs), "W", W, flush=True)


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

pad = (-len(Fs)) % W
s2 = "0" * pad + Fs
chunks = [int(s2[i:i + W]) for i in range(0, len(s2), W)]
print("chunks", len(chunks), "pad", pad, flush=True)
out = "".join(table.get(c, "?") for c in chunks)
print("decoded:", out, flush=True)
for i, c in enumerate(chunks):
    print(i, table.get(c, "MISS"), flush=True)
s.close()
