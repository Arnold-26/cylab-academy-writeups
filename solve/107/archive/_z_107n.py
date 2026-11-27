import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.set_int_max_str_digits(0)
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.3)
cy.login()
cy.req("PUT", "/api/challenges/107/instance/?source=library")
host = port = None
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/107/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(1), int(m.group(2))
        break
alpha = [chr(c) for c in range(32, 127)]
s = socket.create_connection((host, port), timeout=20)
s.settimeout(3)
banner = b""
t0 = time.time()
while time.time() - t0 < 3:
    try:
        c = s.recv(65536)
        if not c:
            break
        banner += c
        if b"give me" in banner:
            break
    except socket.timeout:
        break
flagnum = re.search(r"flag:\s*(\d+)", banner.decode("latin-1", "replace")).group(1)
pairs = []
for ch in alpha:
    s.sendall(ch.encode() + b"\n")
    time.sleep(0.2)
    r = b""
    t0 = time.time()
    while time.time() - t0 < 1.2:
        try:
            c = s.recv(65536)
            if not c:
                break
            r += c
        except socket.timeout:
            break
    m = re.search(rb"(\d{20,})", r)
    if m:
        pairs.append((m.group(1).decode(), ch))
s.close()
print("flag digits:", len(flagnum), "| codes:", len(pairs))
options = []
for code, ch in pairs:
    for k in range(0, 3):
        options.append(("0" * k + code, ch))
options.sort(key=lambda x: -len(x[0]))
L = len(flagnum)
memo = {L: ""}


def solve(pos):
    if pos in memo:
        return memo[pos]
    memo[pos] = None
    for code, ch in options:
        if flagnum.startswith(code, pos):
            r = solve(pos + len(code))
            if r is not None:
                memo[pos] = ch + r
                return memo[pos]
    return None


res = solve(0)
print("resultat:", res)
if res:
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", res)
    print("FLAG:", m.group(0) if m else res)
