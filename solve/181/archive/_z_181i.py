import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = "chatelaine.cylabacademy.net", 15649
s = socket.create_connection((host, port), timeout=15)
s.settimeout(4)
buf = b""


def read_until_prompt(t=6.0):
    global buf
    t0 = time.time()
    while time.time() - t0 < t:
        m = re.search(rb"(\d+)\?", buf)
        if m:
            return int(m.group(1))
        try:
            c = s.recv(4096)
            if not c:
                return None
            buf += c
        except socket.timeout:
            break
    return None


def answer(n):
    if n % 15 == 0:
        return "fizzbuzz"
    if n % 3 == 0:
        return "fizz"
    if n % 5 == 0:
        return "buzz"
    return str(n)


for i in range(120):
    n = read_until_prompt()
    if n is None:
        print("arret a l'iteration %d, tampon: %r" % (i, buf[-300:]))
        break
    # consommer le prompt
    buf = buf[buf.find(b"%d?" % n) + len(b"%d?" % n):]
    a = answer(n)
    s.sendall(a.encode() + b"\n")
    if i < 5 or i % 20 == 0:
        print("  tour %d: %d -> %s" % (i, n, a), flush=True)
time.sleep(0.5)
print("=== fin de boucle, buffer restant ===")
print(buf[-400:])
s.close()
