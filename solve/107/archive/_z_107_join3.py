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
print("F digits", len(str(F)), "n digits", len(str(n)), flush=True)


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
    return m[-1].decode() if m else None


A = ask(b"4")
B = ask(b"1")
AB = ask(b"41")
print("lens", len(A), len(B), len(AB))
print("cat(A,B):", A + B == AB)
print("cat(B,A):", B + A == AB)
print("cat pad:", A + B.zfill(len(A)) == AB, A.zfill(len(B)) + B == AB)
s.close()
