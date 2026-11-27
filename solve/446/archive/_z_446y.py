import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 25092
EXPLOIT = "w" * 3 + "a" * 5 + "w" + "a" * 6 + "d" * 3 + "d" * 3 + "s" + "d"
SEQ = (EXPLOIT + "p") * 6


def attempt():
    s = socket.create_connection((HOST, PORT), timeout=30)
    s.settimeout(20)
    time.sleep(0.5)
    try:
        s.recv(65536)
    except Exception:
        pass
    s.sendall(SEQ.encode())
    found = None
    levels = set()
    t0 = time.time()
    total = 0
    while time.time() - t0 < 100:
        try:
            c = s.recv(65536)
        except socket.timeout:
            break
        if not c:
            break
        total += len(c)
        for m in re.finditer(rb"Level: (\d+)", c):
            levels.add(int(m.group(1)))
        f = re.search(rb"(?:academy|picoCTF)\{[^}]*\}", c)
        if f:
            found = f.group(0).decode()
            break
        if b"No more lives" in c or b"obstacle" in c:
            if b"No more lives" in c:
                break
    s.close()
    return found, sorted(levels), total


for i in range(3):
    found, levels, total = attempt()
    print(f"essai {i}: niveaux={levels} octets={total} flag={found}")
    if found:
        break
