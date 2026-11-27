import socket, sys, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"D:\ctf-index\_z_107url.txt").read().split()
port = int(port)
s = socket.create_connection((host, port), timeout=20)
s.settimeout(3)

buf = b""
def drain(t=2.0):
    global buf
    end = time.time() + t
    while time.time() < end:
        try:
            d = s.recv(65536)
        except socket.timeout:
            break
        if not d:
            break
        buf += d

drain(3.0)
txt = buf.decode("latin-1")
buf = b""
print("banner total chars:", len(txt))
parts = re.split(r"(\n)", txt)
print("nb lignes:", txt.count("\n") + 1)
# affiche un resume par ligne
i = 0
for ln in txt.split("\n"):
    i += 1
    print("L%d len=%d : %s ... %s" % (i, len(ln), ln[:60], ln[-30:]))
print("=== fin banner ===")
open(r"D:\ctf-index\_z_107_banner.txt", "w").write(txt)
