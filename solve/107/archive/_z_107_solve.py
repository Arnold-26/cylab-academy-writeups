import socket, time, re, sys
sys.set_int_max_str_digits(0)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HOST, PORT = "chatelaine.cylabacademy.net", 24284
s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(4)
time.sleep(0.8)
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
s.close()
txt = buf.decode(errors="replace")
print("banner len", len(txt))
m = re.search(r"flag:\s*(\d+)", txt)
mn = re.search(r"n:\s*(\d+)", txt)
me = re.search(r"e:\s*(\d+)", txt)
print("flag digits:", len(m.group(1)) if m else None)
print("n bits:", int(mn.group(1)).bit_length() if mn else None)
print("e:", me.group(1) if me else None)
open(r"./_z_107_banner.txt", "w", encoding="utf-8").write(txt)
F = int(m.group(1)); n = int(mn.group(1)); e = int(me.group(1))

chunks = []
x = F
while x:
    chunks.append(x % n)
    x //= n
print("chunks (base n):", len(chunks))
out = ""
for i, c in enumerate(chunks):
    got = None
    for p in range(32, 127):
        if pow(p, e, n) == c:
            got = chr(p)
            break
    if got is None:
        for p in range(0, 32):
            if pow(p, e, n) == c:
                got = chr(p)
                break
    out += got if got else "?"
print("decoded:", out)
