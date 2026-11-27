# 473 - Guess My Cheese (Part 1)  (Cryptography, picoCTF 2025)
# Flag: academy{ChEeSy8b0897b1}
# Write-up: ../../../writeups/cryptography/473-guess-my-cheese-part-1.md
# Script exact utilise pour produire le flag.
#
import sys, re, time, socket, json

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def enc(pt, a, b):
    return "".join(UP[(a * UP.index(c) + b) % 26] for c in pt.upper() if c in UP)


def dec(ct, a, b):
    ai = pow(a, -1, 26)
    return "".join(UP[(ai * (UP.index(c) - b)) % 26] for c in ct.upper() if c in UP)


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
s = socket.create_connection((host, port), timeout=20)
s.settimeout(6)
time.sleep(0.6)


def rd(t=1.5, stop=b"like to do?"):
    s.settimeout(t)
    buf = b""
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            c = s.recv(16384)
            if not c:
                break
            buf += c
            if stop in buf:
                break
        except socket.timeout:
            break
    return buf.decode("utf-8", "replace")


banner = rd(2.0)
m = re.search(r"guess it:\s+([A-Z]+)", banner)
secret = m.group(1) if m else None
print("secret:", secret)
s.sendall(b"e\n"); time.sleep(0.3); rd(1.0)
s.sendall(b"CHEDDAR\n"); time.sleep(0.4)
r = rd(1.5)
ct = None
for mm in re.finditer(r"\b([A-Z]{7})\b", r):
    if mm.group(1) != "CHEDDAR":
        ct = mm.group(1)
print("CT:", ct)
key = None
if ct:
    for a in (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25):
        for b in range(26):
            if enc("CHEDDAR", a, b) == ct:
                key = (a, b)
                break
        if key:
            break
print("cle:", key)
if key and secret:
    pt = dec(secret, *key)
    print("fromage:", pt, "| lowercase:", pt.lower())
    for cand in (pt, pt.lower()):
        s.sendall(b"g\n"); time.sleep(0.3); rd(1.0)
        s.sendall((cand + "\n").encode())
        time.sleep(0.5)
        r2 = rd(2.0)
        print(f"--- essai {cand} ---")
        print(r2[:500])
        fl = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r2)
        if fl:
            print("FLAG:", fl.group(0))
            break
s.close()
