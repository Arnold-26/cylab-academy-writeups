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

for probe in (b"41", b"1234", b"abc"):
    s.sendall(probe + b"\n")
    time.sleep(0.6)
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
    t = out.decode(errors="replace")
    m = re.search(r"(\d{50,})", t)
    if not m:
        print(probe, "no ciphertext:", t[:200])
        continue
    C = int(m.group(1))
    cands = {
        "int('41')": int(probe),
        "int(hex)": int(probe, 16),
        "from_bytes": int.from_bytes(probe, "big"),
    }
    hit = [k for k, v in cands.items() if pow(v % n, e, n) == C]
    print(probe, "-> hits:", hit, "bits:", C.bit_length())
s.close()
