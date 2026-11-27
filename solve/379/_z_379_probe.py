import socket, sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = open("/mnt/d/ctf-index/_z_379url.txt").read().split()
s = socket.create_connection((HOST, int(PORT)), timeout=30)
s.settimeout(10)
buf = b""
while b"vainglory?" not in buf:
    d = s.recv(65536)
    if not d:
        break
    buf += d
txt = buf.decode()
print(txt)
m1 = re.search(r"anger = (\d+)", txt)
m2 = re.search(r"envy = (\d+)", txt)
ct = int(m1.group(1)); dval = int(m2.group(1))
K = 65537 * dval - 1
print("ct bits:", ct.bit_length(), "d bits:", dval.bit_length(), "K bits:", K.bit_length())
open("/mnt/d/ctf-index/_z_379_data.txt", "w").write("%d\n%d\n" % (ct, dval))
# trial division rapide
import sympy
rem = K
fs = []
p = 2
while p < 200000 and rem > 1:
    if rem % p == 0:
        e = 0
        while rem % p == 0:
            rem //= p; e += 1
        fs.append((p, e))
    p = sympy.nextprime(p)
print("petits facteurs:", fs)
print("cofacteur:", rem, "bits:", rem.bit_length())
print("cofacteur premier ?", sympy.isprime(rem))
s.close()
