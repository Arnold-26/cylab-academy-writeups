import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 17503
UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def affine_enc(pt, a, b):
    return "".join(UP[(a * UP.index(c) + b) % 26] if c in UP else c for c in pt.upper())


def affine_dec(ct, a, b):
    ainv = pow(a, -1, 26)
    return "".join(UP[(ainv * (UP.index(c) - b)) % 26] if c in UP else c for c in ct.upper())


s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(6)
time.sleep(0.6)


def rd(t=1.5):
    s.settimeout(t)
    buf = b""
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            c = s.recv(16384)
            if not c:
                break
            buf += c
            if b"like to do?" in buf:
                break
        except socket.timeout:
            break
    return buf.decode("utf-8", "replace")


banner = rd()
m = re.search(r"secret cheese -- if you're Squeexy, you'll be able to guess it:\s+([A-Z]+)", banner)
secret_ct = m.group(1) if m else None
print("secret CT:", secret_ct)
# demander l'encryption de CHEDDAR
s.sendall(b"e\n")
time.sleep(0.3)
rd(1.0)
s.sendall(b"CHEDDAR\n")
time.sleep(0.4)
r = rd(1.5)
print("reponse oracle:", r[-300:])
m2 = re.search(r"(?:encrypt(?:ed)?[^A-Z]{0,40})([A-Z]{5,})", r)
ct = None
for mm in re.finditer(r"\b([A-Z]{7})\b", r):
    if mm.group(1) != "CHEDDAR":
        ct = mm.group(1)
print("CT de CHEDDAR:", ct)
if ct:
    key = None
    for a in (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25):
        for b in range(26):
            if affine_enc("CHEDDAR", a, b) == ct:
                key = (a, b)
                break
        if key:
            break
    print("cle:", key)
    if key and secret_ct:
        pt = affine_dec(secret_ct, *key)
        print("fromage secret:", pt)
        s.sendall(b"g\n")
        time.sleep(0.3)
        rd(1.0)
        s.sendall((pt + "\n").encode())
        time.sleep(0.5)
        r2 = rd(2.0)
        print("=== REPONSE ===")
        print(r2[:600])
s.close()
